import twint
c = twint.Config()
#tìm kiếm bài viết trong vùng lưu ra file csv. vd file hanoi.csv
c.Since = "2020-02-01"
c.Until = "2020-03-01"
#c.Geo = "10.77976,106.69996,20km"
c.Geo = "21.0278,105.8342 ,20km"
c.Store_csv = True
c.Output = "hanoi_feb.csv"
twint.run.Search(c)
