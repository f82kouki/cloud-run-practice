from fastapi import APIRouter, Query
from app.models import ScoutMessage

router = APIRouter()

MOCK_SCOUTS = [
    ScoutMessage(id=1, student_id=1, student_name="田中 美咲", student_university="早稲田大学",
                 subject="【データ分析】あなたの分析スキルに注目しています", status="accepted",
                 sent_at="2026-03-28T10:00:00+09:00", responded_at="2026-03-29T14:30:00+09:00"),
    ScoutMessage(id=2, student_id=2, student_name="鈴木 大翔", student_university="東京大学",
                 subject="【エンジニア】SaaS開発経験を活かしませんか？", status="accepted",
                 sent_at="2026-03-28T10:15:00+09:00", responded_at="2026-03-28T18:00:00+09:00"),
    ScoutMessage(id=3, student_id=4, student_name="高橋 蓮", student_university="東京工業大学",
                 subject="【フロントエンド】ハッカソン優勝者のあなたへ特別オファー", status="opened",
                 sent_at="2026-03-29T09:00:00+09:00", responded_at=None),
    ScoutMessage(id=4, student_id=5, student_name="伊藤 結衣", student_university="上智大学",
                 subject="【グローバル人材】語学力を活かせるポジションのご案内", status="declined",
                 sent_at="2026-03-29T09:30:00+09:00", responded_at="2026-03-30T10:00:00+09:00"),
    ScoutMessage(id=5, student_id=6, student_name="渡辺 陸", student_university="大阪大学",
                 subject="【AI/ML】自然言語処理の研究経験を活かしませんか", status="opened",
                 sent_at="2026-03-30T11:00:00+09:00", responded_at=None),
    ScoutMessage(id=6, student_id=8, student_name="中村 翔太", student_university="筑波大学",
                 subject="【バックエンド】大規模開発の即戦力として", status="pending",
                 sent_at="2026-03-31T14:00:00+09:00", responded_at=None),
    ScoutMessage(id=7, student_id=10, student_name="加藤 悠人", student_university="京都大学",
                 subject="【リーガルテック】法律×技術の新規事業を一緒に", status="pending",
                 sent_at="2026-03-31T15:00:00+09:00", responded_at=None),
    ScoutMessage(id=8, student_id=3, student_name="佐藤 花", student_university="慶應義塾大学",
                 subject="【マーケター】SNS運用の実績に感銘を受けました", status="accepted",
                 sent_at="2026-03-27T10:00:00+09:00", responded_at="2026-03-28T09:00:00+09:00"),
    ScoutMessage(id=9, student_id=9, student_name="小林 さくら", student_university="お茶の水女子大学",
                 subject="【データサイエンス】バイオ×ITの新領域へ", status="pending",
                 sent_at="2026-04-01T09:00:00+09:00", responded_at=None),
    ScoutMessage(id=10, student_id=7, student_name="山本 愛", student_university="明治大学",
                 subject="【ファイナンス】財務分析スキルを当社で発揮しませんか", status="opened",
                 sent_at="2026-04-01T10:00:00+09:00", responded_at=None),
]


@router.get("/scouts", response_model=list[ScoutMessage])
def get_scouts(
    status: str | None = Query(None, description="ステータスで絞り込み"),
):
    if status:
        return [s for s in MOCK_SCOUTS if s.status == status]
    return MOCK_SCOUTS
