class NewsModel:
    def __init__(self, title, date, description, picture, count, contains_money):
        self.title = title
        self.date = date
        self.description = description          # description (if available)
        self.picture = picture                  # picture filename
        self.count = count                      # count of search phrases in the title and description
        self.contains_money = contains_money    # - True or False, depending on whether the title or description contains any amount of money
                                                    # Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD


