class Course
  include MongoMapper::Document

  key :name, String
  key :dirty, Boolean

end
