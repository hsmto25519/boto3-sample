# boto3-sample

* STSから一時認証情報を取得
* KMSを使って暗号化・復号

## Requirements

### 前提
- Python 3.12
- pip 24.3
- AWSのアクセスキー設定済み
- MFA設定済み
- IAMの権限設定済み

### KMS key作成
```
# in ./terraform
terraform apply
```

### Dependenciesのインストール
requirements.txtは作成してあるため、以下でインストール可能

``` bash
pip install -r requirements.txt
```

## プログラム実行
```
# in ./src
python main.py <mfa_code>
# 例. python main.py 555555
```