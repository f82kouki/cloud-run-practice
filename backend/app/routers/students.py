from fastapi import APIRouter, Query
from app.models import Student

router = APIRouter()

MOCK_STUDENTS = [
    Student(
        id=1, name="田中 美咲", university="早稲田大学", faculty="商学部",
        graduation_year=2027, skills=["Python", "データ分析", "Tableau"],
        desired_industries=["IT", "コンサル"], self_pr="データサイエンスコンペで入賞経験あり。ビジネス課題をデータで解決することに関心があります。",
        last_login="2026-04-01T10:30:00+09:00",
    ),
    Student(
        id=2, name="鈴木 大翔", university="東京大学", faculty="工学部",
        graduation_year=2027, skills=["Go", "Kubernetes", "AWS"],
        desired_industries=["IT", "メーカー"], self_pr="個人開発でSaaSアプリをリリースし、月間1000ユーザーを達成しました。",
        last_login="2026-04-01T09:15:00+09:00",
    ),
    Student(
        id=3, name="佐藤 花", university="慶應義塾大学", faculty="経済学部",
        graduation_year=2027, skills=["マーケティング", "SNS運用", "Figma"],
        desired_industries=["広告", "メディア"], self_pr="学生団体でSNSフォロワー1万人のアカウントを運用。マーケティング戦略を立案しました。",
        last_login="2026-03-31T22:00:00+09:00",
    ),
    Student(
        id=4, name="高橋 蓮", university="東京工業大学", faculty="情報理工学院",
        graduation_year=2027, skills=["React", "TypeScript", "Next.js"],
        desired_industries=["IT", "スタートアップ"], self_pr="ハッカソンで3度の優勝経験。フロントエンド開発を得意としています。",
        last_login="2026-04-01T08:45:00+09:00",
    ),
    Student(
        id=5, name="伊藤 結衣", university="上智大学", faculty="外国語学部",
        graduation_year=2027, skills=["英語(TOEIC950)", "中国語", "プレゼン"],
        desired_industries=["商社", "コンサル"], self_pr="留学経験を活かし、日英中のトリリンガルとしてグローバルビジネスに貢献したいです。",
        last_login="2026-03-31T20:30:00+09:00",
    ),
    Student(
        id=6, name="渡辺 陸", university="大阪大学", faculty="基礎工学部",
        graduation_year=2027, skills=["Python", "機械学習", "PyTorch"],
        desired_industries=["IT", "研究機関"], self_pr="自然言語処理の研究に取り組んでおり、国際学会でポスター発表の経験があります。",
        last_login="2026-04-01T11:00:00+09:00",
    ),
    Student(
        id=7, name="山本 愛", university="明治大学", faculty="政治経済学部",
        graduation_year=2028, skills=["Excel", "財務分析", "簿記2級"],
        desired_industries=["金融", "コンサル"], self_pr="投資サークルの代表として、実際の株式ポートフォリオ運用を経験しました。",
        last_login="2026-03-30T18:00:00+09:00",
    ),
    Student(
        id=8, name="中村 翔太", university="筑波大学", faculty="情報学群",
        graduation_year=2027, skills=["Java", "Spring Boot", "Docker"],
        desired_industries=["IT", "SIer"], self_pr="長期インターンで大規模Webサービスのバックエンド開発に1年間従事しました。",
        last_login="2026-04-01T07:30:00+09:00",
    ),
    Student(
        id=9, name="小林 さくら", university="お茶の水女子大学", faculty="理学部",
        graduation_year=2028, skills=["R", "統計学", "生物情報学"],
        desired_industries=["製薬", "IT", "研究機関"], self_pr="バイオインフォマティクスを専攻し、ゲノムデータ解析パイプラインを構築しています。",
        last_login="2026-03-31T15:20:00+09:00",
    ),
    Student(
        id=10, name="加藤 悠人", university="京都大学", faculty="法学部",
        graduation_year=2027, skills=["リーガルテック", "契約書レビュー", "法務"],
        desired_industries=["IT", "法律事務所"], self_pr="法律×テクノロジーの領域に興味があり、契約書自動レビューツールを個人開発中です。",
        last_login="2026-04-01T12:00:00+09:00",
    ),
]


@router.get("/students", response_model=list[Student])
def get_students(
    industry: str | None = Query(None, description="希望業界で絞り込み"),
    graduation_year: int | None = Query(None, description="卒業年度で絞り込み"),
):
    results = MOCK_STUDENTS
    if industry:
        results = [s for s in results if industry in s.desired_industries]
    if graduation_year:
        results = [s for s in results if s.graduation_year == graduation_year]
    return results
