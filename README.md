# 赤兎馬のスクレイピングコード
全てのファイル単体で完結している。  
全てのファイルでpickleでAWSのS3に保存される。main_data_collect.pyが基準となっている。

## ファイルの説明
以下で各ファイルの説明と作成データの説明を行う。

### main_data_collect.py
2009~2020までのデータ収集を行う。  
ここで作成されるデータをベースに他のデータの収集を行う。

1. horce_url.pickle 
   - [馬の名前] = 馬のURL
2. race_data.pickle
   - [レースのURL][馬の名前] = []
3. jockey_name.pickle
   - [騎手のURL] = 騎手の名前
4. horce_data_storage.pickle
   - [馬の名前] = レースの文字列リスト
   
### baba_index.py
horce_url.pickleから各レースの馬場指数を収集する。

1. baba_index_data.pickle
   - [馬の名前][生年月日] = 馬場指数
   
### blood_data_get.py
horce_url.pickleからクロスの血統とその割合を収集する。

1. blood_closs_data.pickle
   - [馬の名前] = { "name": 血統のクロスの名前, "rate": 割合(%) }
   
### father_data.py
horce_url.pickleから父親の産駒の情報を取得する。

1. father_name.pickle
   - [馬の名前] = 父親の馬の名前
2. father_grade_data.pickle
   - [馬の名前][年(西暦)] = { "go_num": 出走頭数, "win_num": 勝った馬の数, "win_rate": 勝率, "EI": EI }
3. father_condition_grade.pickle
   - [馬の名前]["kb"]["1400"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["1800"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["2200"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["2600"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["2601"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["1"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["2"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["3"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["4"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   
### first_time_get.py
race_data.pickleから馬ごとの過去5レースの前半3Fのデータを収集する。

1. first_time.pickle
   - [race_id] = { "name": 馬の名前, "time": 前半3Fのリスト }のリスト
   
### horce_data_collect.py
horce_url.pickleから調教師のURLと性別などの馬の情報を収集する。

1. horce_data.pickle 
   - [馬の名前]["sex"] = 性別
   - [馬の名前]["birth"] = 生まれ年
   - [馬の名前]["trainer"] = 調教師名
   - [馬の名前]["charactor"] = { "course": 芝かダート, "dist": 長いか短い, "foot": 逃げか追い込みか, "growth": 早熟か晩成, "heavy_baba": 重馬場が得意か苦手 }
   
2. trainer_url.pickle
   - [調教師の名前] = 調教師のURL

### jockey_data.py
jockey_name.pickleから騎手の年ごとの勝率,連対率,複勝率を収集する。
1. jockey_data.pickle
   - [騎手のURL][西暦] = [ 勝率, 連対率, 複勝率 ]

### jockey_full_data_collect.py
jockey_name.pickleから全てのレースの騎手の情報を収集する。
1. jockey_full_data.pickle
   - [騎手のURL][生年月日][レース番号]["place"] = 場所
   - [騎手のURL][生年月日][レース番号]["weather"] = 天気
   - [騎手のURL][生年月日][レース番号]["all_horce_num"] = 出走頭数
   - [騎手のURL][生年月日][レース番号]["flame_num"] = 枠番
   - [騎手のURL][生年月日][レース番号]["horce_num"] = 馬番
   - [騎手のURL][生年月日][レース番号]["odds"] = オッズ
   - [騎手のURL][生年月日][レース番号]["popular"] = 人気
   - [騎手のURL][生年月日][レース番号]["rank"] = 順位
   - [騎手のURL][生年月日][レース番号]["weight"] = 馬体重
   - [騎手のURL][生年月日][レース番号]["dist"] = 距離
   - [騎手のURL][生年月日][レース番号]["baba"] = 馬場
   - [騎手のURL][生年月日][レース番号]["time"] = 走破タイム
   - [騎手のURL][生年月日][レース番号]["diff"] = 着差

### jockey_money_collect.py
jockey_name.pickleから騎手の年間の獲得賞金を取得する。
1. jockey_money_data.pickle
   - [騎手のURL][西暦] = 獲得賞金

### limb_collect.py
race_data.pickleから各レースの競馬新聞に記載されている脚質を取得する。
逃げ:1 先行:2 差し:3 追い込み:4 それ以外:0 となっている。
1. limb_data.pickle
   - [race_id][馬の名前] = 脚質の数値

### odds_collect.py
race_data.pickleから各レースの確定のオッズを収集する。
1. odds_data.pickle
   - [race_id]["単勝"] = 単勝のオッズ
   - [race_id]["複勝"] = 複勝のオッズのリスト (順位の順)
   - [race_id]["馬連"] = 馬連のオッズ
   - [race_id]["ワイド"] = ワイドのオッズのリスト
   - [race_id]["馬単"] = 馬単のオッズ
   - [race_id]["三連複"] = 三連複のオッズ
   - [race_id]["三連単"] = 三連単のオッズ

### omega_index_get.py
https://www.keibalab.jpのサイトにあるオメガ指数を取得する。
1. omega_index_data.pickle
   - [race_id] = オメガ指数のリスト (馬番の順)

### pace_data_collect.py
race_data.pickleからペースH,M,Sを取得する。
1. pace_data.pickle
   - [race_id] = ペースの文字列

### parent_data_collect.py
horce_url.pickleから両親のURLと情報を取得する
1. parent_url_data.pickle
   - [馬の名前]["father"] = 父親のURL
   - [馬の名前]["mother"] = 母親のURL

2. parent_data.pickle
   - [馬の名前]["father"]["dist"] = 走った平均の距離
   - [馬の名前]["father"]["race_kind"] = 走った平均のレースの種類
   - [馬の名前]["father"]["rank"] = 走った平均の順位
   - [馬の名前]["father"]["diff"] = 走った平均の着差
   - [馬の名前]["father"]["up_time"] = 走った平均の上り3F
   - [馬の名前]["mother"]["dist"] = 走った平均の距離
   - [馬の名前]["mother"]["race_kind"] = 走った平均のレースの種類
   - [馬の名前]["mother"]["rank"] = 走った平均の順位
   - [馬の名前]["mother"]["diff"] = 走った平均の着差
   - [馬の名前]["mother"]["up_time"] = 走った平均の上り3F

### passing_data_collect.py
horce_url.pickleから各コーナーの通過順位を収集する。
1. passing_data.pickle
   - [馬の名前][生年月日] = 通過順位の文字列 例:1-2-3-4

### race_course_data.py
race_data.pickleから各レースが外回りかどうかと右か左回りかを収集する。
1. race_course_data.pickle
   - [race_id]["out_side"] = 外回りならTrue 違うならFalse
   - [race_id]["direction"] = 右回りなら1 左回りなら2

### race_day_get.py
race_data.pickleから各レースの生年月日を取得する。
1. race_day.pickle
   - [race_id] = 生年月日

### race_info_collect.py
race_data.pickleとrace_course_data.pickleからレースの情報を収集しまとめる。
1. race_info_data.pickle
   - [race_id]["out_side"] = 外回りならTrue 違うならFalse
   - [race_id]["direction"] = 右回りなら1 左回りなら2
   - [race_id]["kind"] = 芝かダートか
   - [race_id]["dist"] = 距離
   - [race_id]["baba"] = 馬場
   - [race_id]["place"] = 場所

### race_money.py
race_data.pickleから各レースの一位の賞金を収集する。
1. race_money_data.pickle
   - [race_id] = 一位の賞金

### race_start_time_collect.py
race_data.pickleからレースの開始時間を収集する。
1. race_start_time.pickle
   - [race_id]["hour"] = 時間
   - [race_id]["minute"] = 分

### race_time_collect.py
race_data.pickleからタイムを収集する。
1. race_time_data.pickle
   - [race_id]["time"] = タイム
   - [race_id]["dist"] = 距離

### race_up_halon.py
race_data.pickleから前半3Fのタイムを取得する
1. first_yp3_halon.pickle
   - [race_id][馬番] = 前半3Fのタイム

### test_keibarabo.py
動画収集の実験コード。

### train_condition.py
race_data.pickleから調教の馬の評価(A,B,C,D)とコメントを収集する。
1. train_condition.pickle
   - [race_id][馬の名前]["eveluation"] = 評価
   - [race_id][馬の名前]["comment"] = コメント

2. train_condition_chenge.pickle
   - ["eveluation"][評価] = ラベル
   - ["eveluation"][コメント] = ラベル

### traner_collect.py
trainer_url.pickleから調教師の情報を収集する。
1. trainer_data.pickle
   - [調教師名][西暦]["one_rate"] = 勝率
   - [調教師名][西暦]["two_rate"] = 蓮対率
   - [調教師名][西暦]["three_rate"] = 副勝率
   - [調教師名][西暦]["siba_rate"] = 芝の勝率
   - [調教師名][西暦]["date_rate"] = ダートの勝率

### wrap_data_collect.py
race_data.pickleから200mごとのレースのラップタイムを収集する。
1. wrap_data.pickle
   - [race_id][ラップの距離] = ラップタイム


    
   
