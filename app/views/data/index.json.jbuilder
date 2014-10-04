json.array!(@data) do |datum|
  json.extract! datum, :academics
  json.url datum_url(datum, format: :json)
end