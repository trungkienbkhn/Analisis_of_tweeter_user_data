import twint
c = twint.Config()
c.Search = "covid"
c.Store_csv = True
c.Lang = "vi"
c.Since = "2020-04-06"
c.Until = "2020-04-13"
c.Output = "data.csv"
twint.run.Search(c)
