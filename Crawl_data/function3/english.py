import twint
c = twint.Config()
c.Search = "covid"
c.Since = "2020-04-18"
c.Until = "2020-04-23"
c.Lang = "vi"
c.Store_csv = True
c.Output = "content5.csv"
c.Limit = 1000
twint.run.Search(c)
