// Create a text parameter named TrafficCsvPath containing the raw CSV path.
// This implements the required raw import/preparation; audit anomalies before modelling.
let
    Source = Csv.Document(File.Contents(TrafficCsvPath), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"holiday",type text},{"temp",type number},{"rain_1h",type number},{"snow_1h",type number},{"clouds_all",Int64.Type},{"weather_main",type text},{"weather_description",type text},{"date_time",type datetime},{"traffic_volume",Int64.Type}}),
    Hour = Table.AddColumn(Types,"Hour",each Time.Hour(DateTime.Time([date_time])),Int64.Type),
    Celsius = Table.AddColumn(Hour,"Temperature_Celsius",each if [temp]>0 then [temp]-273.15 else null,type number),
    Category = Table.AddColumn(Celsius,"traffic_category_fixed",each if [traffic_volume]<4500 then "Low" else if [traffic_volume]<=5500 then "Medium" else "High",type text),
    Date = Table.AddColumn(Category,"Date",each Date.From([date_time]),type date),
    Year = Table.AddColumn(Date,"Year",each Date.Year([Date]),Int64.Type)
in
    Year
