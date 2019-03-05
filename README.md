このスクリプトは，ToDoistに毎日ランダムに選ばれた「筋肉体操」をタスクとして追加するためのスクリプトです．

AWS Lambdaでの動作を想定しています．
1回の動作時間が10sec程と多少長いですが，毎日1回，128MBの設定で動作させても無料枠に全然問題なく収まるはずです．

# 動作内容
このLambda関数が実行されると，ToDoist上にタスクが1件追加されます．

タスクのnote部分には，YoutubeにあるNHK公式が配信している「筋肉体操」から，ランダムにいくつかが選択されてリンクが記載されます．
同一種目が複数回・複数の内容選択されることはありません．

## タスクのタイトル変更
デフォルトのタイトルは「トレーニング」となっており，プロジェクト「Inbox」に追加されます．
これらは**lambda_function.py**の19-21行目にある
``` python
     project = user.get_project("Inbox")
     task = project.add_task("トレーニング",date=limit)
```
部分を書き換えることで変更できます．

## タスクの締め切り時刻変更
追加されるタスクの締め切り時刻は初期値で22:15となっていますが，**lambda_function.py**の11行目にある
``` python
limit = todo.ConvTime(22,15)
```
の部分を書き換えることで変更可能です．
以下のように，締め切り時刻**HH:MM**ならば
``` python
limit = todo.ConvTime(HH,MM)
```
と書き換えてください．



# インストール手順
## ローカルでの準備
1. このスクリプトをダウンロード
``` bash
git clone git@github.com:thvinmei/AddTodoist_TrainingTask.git M2T
```

2. pytodoistをスクリプトと同じディレクトリにインストール
``` bash
cd M2T
pip install -t .
```

3. zip圧縮
``` bash
zip -r upload.zip *
```

## AWS Lambdaへのアップロード
1. AWS Lambdaの管理画面にログインし，関数を作成
    - "一から作成"を選択
    - ランタイムに"Python3.7"を選択
    - 名前，ロールは任意で．

2. 関数マネジメント画面での設定
    1. トリガーの設定
        - トリガーに"CloudWatch Events"を追加
        - cron式などで1日一回動作するように設定する．

        ``` bash
        # 毎日12:00JST(03:00UTC)に動かす場合
        cron(0 3 * * ? *)
        ```
        - 「保存」
    
    2. Lambda関数のアップロード
        - コードエントリタイプで「.zipファイルをアップロード」を選択
        - 先程作成した，upload.zipを選択
        - 「保存」
    
    3. ハンドラを**lambda_function.Training2Todoist**に設定する
    4. 環境変数の設定
        - キーに**TODOIST_API_TOKEN**，値にToDoistのアカウント設定ページから取得できるAPIトークンを入力
        - キーに**NUMBER_OF_TRAININGS**，値に1日あたりのトレーニング種目数を入力
            - ただし，この値が種目数である4以上になることを想定していません．（ただし，種目数を増やした場合はその限りではないです．）
            - また，この値は整数値で入力が必要です．
    5. 「保存」

## テスト実行
テストイベントは**Amazon CloudWatch**をイベントテンプレートとして作成してください．

テスト実行して，ToDoist側にタスクが追加できていれば完了です．