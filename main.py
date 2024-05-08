import discord
import gspread
import os
import random
from oauth2client.service_account import ServiceAccountCredentials
from keep_alive import keep_alive

# 環境変数の設定
GSS_TEMP_KEY = os.environ['GSS_TEMP_KEY']
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']


class MyClient(discord.Client):

    async def on_ready(self):
        """Discord接続時に実行される関数."""
        print(f'{self.user}として接続しました。')

    async def on_message(self, message: discord.Message):
        """メッセージ受信時に実行される関数."""
        # ボット自身のメッセージは無視する
        if message.author == self.user:
            return

        print(f'{message.author}よりメッセージを受信しました: {message.content}')
        if message.content == '!omikuji':
            choice = random.choice(['大吉', '吉', '小吉', '凶', '大凶'])
            await message.channel.send(f"あなたの今日の運勢は **{choice}** です!")

        if message.content == '!kadai':
            selected_values = create_post_message(
                target=["FAILED", "E-CLEAR", "CLEAR"])
            # 要素ごとに文字列をつなげて出力
            await message.channel.send(
                f"あなたの今日の課題曲は **{selected_values[0]}** です!\n現在のランプ：{selected_values[1]}\n推奨オプション：{selected_values[2]}"
            )

        if message.content == '!easy':
            selected_values = create_post_message(target=["FAILED"])
            # 要素ごとに文字列をつなげて出力
            await message.channel.send(
                f"イージー狙いの課題曲は **{selected_values[0]}** です!\n現在のランプ：{selected_values[1]}\n推奨オプション：{selected_values[2]}"
            )

        if message.content == '!normal':
            selected_values = create_post_message(target=["E-CLEAR"])
            # 要素ごとに文字列をつなげて出力
            await message.channel.send(
                f"ノマゲ狙いの課題曲は **{selected_values[0]}** です!\n現在のランプ：{selected_values[1]}\n推奨オプション：{selected_values[2]}"
            )

        if message.content == '!hard':
            selected_values = create_post_message(target=["CLEAR"])
            # 要素ごとに文字列をつなげて出力
            await message.channel.send(
                f"ハード狙いの課題曲は **{selected_values[0]}** です!\n現在のランプ：{selected_values[1]}\n推奨オプション：{selected_values[2]}"
            )


# worksheetからの取得を行う関数
def create_post_message(target):
    # スプレッドシートを定義
    worksheet = get_gss_worksheet(gss_name='ビートマニア☆１１地力表（マジでがんばれ）',
                                  gss_sheet_name='地力表')
    rows = worksheet.get_all_values()
    # 最初の2行をスキップしてランダムな行を選択
    while True:
        random_row = random.choice(rows[2:])
        # 特定の条件リストに含まれる値と一致するかを確認
        if random_row[11] in target:
            break  # 条件を満たす場合、ループを抜ける

    # 特定の列の値を取得
    columns_to_get = [10, 11, 16]  # 曲名、ランプ、推奨OP
    selected_values = [random_row[col] for col in columns_to_get]

    return selected_values


# worksheetの情報を返す関数
def get_gss_worksheet(gss_name, gss_sheet_name):
    #jsonファイルを使って認証情報を取得
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    c = ServiceAccountCredentials.from_json_keyfile_name(
        'gss_credential.json', scope)
    #認証情報を使ってスプレッドシートの操作権を取得
    gs = gspread.authorize(c)
    # スプレッドシート名をもとに、キーを設定
    if gss_name == "ビートマニア☆１１地力表（マジでがんばれ）":
        spreadsheet_key = GSS_TEMP_KEY
    #共有したスプレッドシートのキーを使ってシートの情報を取得
    worksheet = gs.open_by_key(spreadsheet_key).worksheet(gss_sheet_name)

    return worksheet


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
keep_alive()
try:
    client.run(DISCORD_TOKEN)
except:
    os.system("kill 1")
