json.array!(@courses) do |course|
  json.extract! course, :name, :dirty
  json.url course_url(course, format: :json)
end