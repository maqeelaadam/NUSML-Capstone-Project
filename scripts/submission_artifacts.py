"""Build, restore or verify the portable models and original MLflow records."""
import argparse
import hashlib
import json
import logging
from pathlib import Path, PurePosixPath
import shutil
import zipfile

logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'capstone_part3/artifacts/verified_models.zip'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def packaged_files(archive):
    manifest = json.loads(archive.read('manifest.json'))
    if manifest['format_version'] != 1:
        raise ValueError('Unsupported artifact manifest version')
    names = [entry['path'] for entry in manifest['files']]
    if len(names) != len(set(names)) or set(archive.namelist()) != set(names + ['manifest.json']):
        raise ValueError('Archive entries do not match the manifest')
    for entry in manifest['files']:
        path = PurePosixPath(entry['path'])
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Unsafe archive path')
        if not (entry['path'].startswith('capstone_part3/models/') or
                entry['path'].startswith('.runtime/mlruns/')):
            raise ValueError('Unexpected archive destination')
        data = archive.read(entry['path'])
        if len(data) != entry['bytes'] or digest(data) != entry['sha256']:
            raise ValueError(f'Checksum mismatch: {entry["path"]}')
    return manifest


def relocated(path, data):
    """Keep original metrics/timestamps; only relocate MLflow file URIs."""
    if not path.endswith('/meta.yaml') or not path.startswith('.runtime/mlruns/'):
        return data
    lines = data.decode('utf-8').splitlines()
    folder = ROOT / PurePosixPath(path).parent
    output = []
    for line in lines:
        if line.startswith('artifact_location:'):
            line = 'artifact_location: ' + folder.as_uri()
        elif line.startswith('artifact_uri:'):
            line = 'artifact_uri: ' + (folder / 'artifacts').as_uri()
        output.append(line)
    return ('\n'.join(output) + '\n').encode('utf-8')


def build():
    exports = json.loads((ROOT / 'capstone_part3/experiments/tracking_export.json').read_text())
    comparison = json.loads((ROOT / 'capstone_part3/results/model_comparison.json').read_text())
    records = {entry['mlflow_run_id']: entry for entry in comparison['models']}
    if set(records) != {run['run_id'] for run in exports} or len(records) != 5:
        raise ValueError('Expected exactly the five reported model runs')
    payloads = {}
    copies = []
    runs = []
    for run in exports:
        record = records[run['run_id']]
        model_path = record['model_artifact']
        model_data = (ROOT / model_path).read_bytes()
        payloads[model_path] = model_data
        candidates = list((ROOT / '.runtime/mlruns').glob('*/' + run['run_id']))
        if len(candidates) != 1:
            raise ValueError('Original run folder missing or ambiguous')
        run_folder = candidates[0]
        original_model = run_folder / 'artifacts/models' / Path(model_path).name
        if digest(original_model.read_bytes()) != digest(model_data):
            raise ValueError('Model bytes differ from their original MLflow artifact')
        copies.append({'source': model_path, 'destination': original_model.relative_to(ROOT).as_posix()})
        experiment_meta = run_folder.parent / 'meta.yaml'
        payloads[experiment_meta.relative_to(ROOT).as_posix()] = experiment_meta.read_bytes()
        for file in sorted(run_folder.rglob('*')):
            if file.is_file() and file != original_model:
                payloads[file.relative_to(ROOT).as_posix()] = file.read_bytes()
        runs.append({'run_id': run['run_id'], 'model': model_path,
                     'experiment_id': run_folder.parent.name})
    selected = 'capstone_part3/models/' + comparison['selected_regression'] + '.joblib'
    if digest((ROOT / 'capstone_part3/models/traffic_model.joblib').read_bytes()) != digest(payloads[selected]):
        raise ValueError('Selected model alias does not match the reported selection')
    copies.append({'source': selected, 'destination': 'capstone_part3/models/traffic_model.joblib'})
    manifest = {'format_version': 1, 'source': 'Verified original training outputs; no retraining',
                'python_environment': 'Python 3.12; requirements-lock.txt',
                'runs': runs, 'copies': copies,
                'files': [{'path': path, 'bytes': len(data), 'sha256': digest(data)}
                          for path, data in sorted(payloads.items())]}
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ARCHIVE, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.writestr('manifest.json', json.dumps(manifest, indent=2) + '\n')
        for path, data in sorted(payloads.items()):
            archive.writestr(path, data)
    with zipfile.ZipFile(ARCHIVE) as archive:
        packaged_files(archive)
    summary = {'archive': ARCHIVE.relative_to(ROOT).as_posix(),
               'archive_sha256': digest(ARCHIVE.read_bytes()), 'archive_bytes': ARCHIVE.stat().st_size,
               'model_count': 5, 'original_run_count': 5, 'manifest_file_count': len(payloads)}
    (ARCHIVE.parent / 'archive_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    logger.info('Packaged five models and five original runs: %s (%d bytes)', ARCHIVE, ARCHIVE.stat().st_size)


def restore():
    with zipfile.ZipFile(ARCHIVE) as archive:
        manifest = packaged_files(archive)
        # Validate every member before writing any output.
        for entry in manifest['files']:
            path = entry['path']
            target = ROOT / path
            if not target.resolve().is_relative_to(ROOT.resolve()):
                raise ValueError('Archive destination escapes the checkout')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(relocated(path, archive.read(path)))
        for copy in manifest['copies']:
            source, target = ROOT / copy['source'], ROOT / copy['destination']
            if not target.resolve().is_relative_to(ROOT.resolve()):
                raise ValueError('Copy destination escapes the checkout')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    verify()
    logger.info('Restored models and MLflow records to this checkout without retraining')


def verify():
    summary = json.loads((ARCHIVE.parent / 'archive_summary.json').read_text())
    if digest(ARCHIVE.read_bytes()) != summary['archive_sha256']:
        raise ValueError('Archive checksum does not match archive_summary.json')
    with zipfile.ZipFile(ARCHIVE) as archive:
        manifest = packaged_files(archive)
        for entry in manifest['files']:
            expected = relocated(entry['path'], archive.read(entry['path']))
            if (ROOT / entry['path']).read_bytes() != expected:
                raise ValueError('Restored file differs: ' + entry['path'])
        for copy in manifest['copies']:
            if (ROOT / copy['source']).read_bytes() != (ROOT / copy['destination']).read_bytes():
                raise ValueError('Restored model copy differs: ' + copy['destination'])
    logger.info('Verified every archived/restored checksum, five model pipelines and five run records')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'restore', 'verify'])
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
                        handlers=[logging.StreamHandler(), logging.FileHandler(ROOT / 'submission_artifacts.log', encoding='utf-8')], force=True)
    try:
        {'build': build, 'restore': restore, 'verify': verify}[args.command]()
        return 0
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        logger.error('Artifact operation failed: %s', exc, exc_info=True)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
