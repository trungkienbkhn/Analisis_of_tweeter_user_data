# Đề tài: Phân tích dữ liệu người dùng twitter

> Đồ án các công nghệ xây dựng hệ thống thông tin, trường đại học Bách Khoa Hà Nội

## Các chức năng chính

1. Phân tích xu hướng người dùng thông qua hashtag
2. Phân tích location người dùng quan tâm tới một keyword
3. Phân tích cảm xúc bài viêt
4. Phân tích trending và cảm xúc bài viết thông qua keyword(Ex: covid)

## Requirements

- Postgresql
- Python3
- twint
- pandas
- matplotlib
- geopy
- nltk
- PyQt5
- psycopg2
- pyvi
- scikit-learn
- tensorflow
- Keras

## Installing

> Hệ điều hành yêu cầu: Ubuntu

### Clone

```bash
git clone https://gitlab.com/is_soict/it4434_20192/3_hieunk.git
```

### Postgresql

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### Import database

```bash 
sudo ./start.sh
```

### Install module 

```bash
pip3 install -r requirements.txt
```

### Run

```bash
sudo ./run.sh
```

or

```bash
cd GUI
python3 app.py
```

## Team

- Nguyễn Trung Kiên
- Nguyễn Phú Tài
- Lê Anh Hào
- Nguyễn Minh Sơn
- Nguyễn Thị Hoài Anh
