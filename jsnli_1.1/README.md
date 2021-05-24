== 日本語SNLI(JSNLI)データセット ==

SNLI コーパスを日本語に翻訳した自然言語推論データセット
学習データは元データを翻訳し、計算機によるフィルタリングによって作成
評価データは日本語として意味が通るか、翻訳後のラベルが元のラベルと一致しているかどうかの2段階のクラウドソーシングによりデータをフィルタリング


== ファイル ==

・train_wo_filtering.txt (548,014ペア)
SNLIの学習データに機械翻訳を適用したもの。フィルタリングは行っていない。

・train_w_filtering.txt (533,005ペア) SNLIの学習データに機械翻訳を適用した後、BLEUスコアの閾値0.1でフィルタリングを施したもの。BERTにこの学習データを学習させることにより、93.0%の精度を記録した。

・dev.txt (3,916ペア)
SNLIの評価データに機械翻訳を適用した後、日本語として意味が通るか、ラベルが正しいかどうかの2段階のクラウドソーシングによりデータをフィルタリングしたもの。


==   フォーマット ==

TSV フォーマットで、各行がラベル、前提、仮説の三つ組を表す。

例) entailment      自転車 で ２ 人 の 男性 が レース で 競い ます 。       人々 は 自転車 に 乗って います 。

カラム1 : entailment, contradiction, neutralの3値
カラム2 : 自然言語推論における前提
カラム3 : 自然言語推論における仮説


== ライセンス ==

このデータセットのライセンスは、SNLIのライセンスと同じ CC BY-SA 4.0 に従う。


== 問い合わせ ==

本データセットに関するご質問は nl-resource あっと nlp.ist.i.kyoto-u.ac.jp 宛にお願いいたします。


== 参考文献 == 

・日本語SNLI (JSNLI) データセット

吉越 卓見, 河原 大輔, 黒橋 禎夫:
機械翻訳を用いた自然言語推論データセットの多言語化,
第244回自然言語処理研究会,  (2020.7.3)

・SNLI コーパス

Samuel R. Bowman, Gabor Angeli, Christopher Potts, and Christopher D. Manning. 2015. A large annotated corpus for learning natural language inference. In Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing (EMNLP).

Peter Young, Alice Lai, Micah Hodosh, and Julia Hockenmaier. "From image descriptions to visual denotations: New similarity metrics for semantic inference over event descriptions." Transactions of the Association for Computational Linguistics 2 (2014): 67-78.


