json.array!(@linear_models) do |linear_model|
  json.extract! linear_model, :class1, :class2, :model
  json.url linear_model_url(linear_model, format: :json)
end