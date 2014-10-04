require 'json'

class Datum
  include MongoMapper::Document

  key :input, String
  key :academics, Hash

  before_save :parse_input

  private
  def parse_input
    @academics = JSON.parse(input)
  end

end
