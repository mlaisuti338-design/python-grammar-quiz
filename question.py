questions = [
    {
        "id": 1,
        "question": "文字列を表示するために空欄に入る関数名は？",
        "code": "______('Hello')",
        "answer": "print",
        "hints": [
            "画面に出力する関数",
            "最初に学ぶことが多い"
        ],
        "explanation": "print は、指定した内容を画面に表示するための関数です。"
    },
    {
        "id": 2,
        "question": "変数 x に 10 を代入するとき、空欄に入る記号は？",
        "code": "x ____ 10",
        "answer": "=",
        "hints": [
            "比較ではない",
            "代入を表す記号"
        ],
        "explanation": "= は代入演算子で、右の値を左の変数に入れる意味があります。"
    },
    {
        "id": 3,
        "question": "for文で 0〜4 を繰り返すとき、空欄に入る関数名は？",
        "code": "for i in _____(5):",
        "answer": "range",
        "hints": [
            "連続した数値を作る",
            "0 から始まる"
        ],
        "explanation": "range(5) は 0 から 4 までの数値を順に生成します。"
    },
    {
        "id": 4,
        "question": "条件分岐で使うキーワードは？",
        "code": "_____ x > 5:",
        "answer": "if",
        "hints": [
            "条件が真のときに実行",
            "else とセットで使うこともある"
        ],
        "explanation": "if は、条件が成り立つ場合に処理を実行するための文です。"
    },
    {
        "id": 5,
        "question": "リスト nums の要素数を取得する関数名は？",
        "code": "_____(nums)",
        "answer": "len",
        "hints": [
            "長さを調べる",
            "length の略"
        ],
        "explanation": "len は、リストや文字列などの要素数を取得する関数です。"
    },
    {
        "id": 6,
        "question": "関数を定義するときに使うキーワードは？",
        "code": "_____ add(a, b):",
        "answer": "def",
        "hints": [
            "define の略",
            "関数定義の最初に書く"
        ],
        "explanation": "def は、新しい関数を定義するためのキーワードです。"
    },
    {
        "id": 7,
        "question": "リスト nums に要素を追加するときに使うメソッド名は？",
        "code": "nums._____(4)",
        "answer": "append",
        "hints": [
            "末尾に追加する",
            "add ではない"
        ],
        "explanation": "append は、リストの末尾に新しい要素を追加します。"
    },
    {
        "id": 8,
        "question": "辞書 dic からキー 'a' の値を取り出すとき、空欄に入る記号は？",
        "code": "dic_____'a'",
        "answer": "['",
        "hints": [
            "リストや辞書で使う",
            "角括弧を使う"
        ],
        "explanation": "辞書では、角括弧 [] を使ってキーを指定し、対応する値を取得します。"
    },
    {
        "id": 9,
        "question": "条件が成り立つ間、繰り返す文のキーワードは？",
        "code": "_____ x < 5:",
        "answer": "while",
        "hints": [
            "for ではない",
            "条件が真の間続く"
        ],
        "explanation": "while は、条件が真である間、処理を繰り返す文です。"
    },
    {
        "id": 10,
        "question": "コメントを書くときに使う記号は？",
        "code": "_____ これはコメントです",
        "answer": "#",
        "hints": [
            "この行は実行されない",
            "シャープ記号"
        ],
        "explanation": "# から始まる行はコメントとなり、プログラムとして実行されません。"
    },
    {
        "id": 11,
        "question": "文字列を大文字に変換するメソッドは？",
        "code": "s = 'hello'\ns._____()",
        "answer": "upper",
        "hints": [
            "文字列を大文字に変換",
            "小文字を全部大文字に"
        ],
        "explanation": "upper() メソッドは文字列を大文字に変換します。"
    },
    {
        "id": 12,
        "question": "文字列を小文字に変換するメソッドは？",
        "code": "s = 'HELLO'\ns._____()",
        "answer": "lower",
        "hints": [
            "文字列を小文字に変換",
            "upper の逆"
        ],
        "explanation": "lower() メソッドは文字列を小文字に変換します。"
    },
    {
        "id": 13,
        "question": "リスト nums の先頭要素を取り出すメソッドは？",
        "code": "first = nums._____()",
        "answer": "pop",
        "hints": [
            "最後の要素ではない",
            "pop() は引数にインデックスを指定できる"
        ],
        "explanation": "pop(0) を使うとリストの先頭要素を取り出せます。"
    },
    {
        "id": 14,
        "question": "2つの文字列を結合する演算子は？",
        "code": "'Hello' _____ 'World'",
        "answer": "+",
        "hints": [
            "連結する演算子",
            "数字の足し算でも使う"
        ],
        "explanation": "文字列は + 演算子で結合できます。"
    },
    {
        "id": 15,
        "question": "リストから要素を削除するときのメソッドは？",
        "code": "nums._____('a')",
        "answer": "remove",
        "hints": [
            "値を指定して削除",
            "pop と違ってインデックス不要"
        ],
        "explanation": "remove() メソッドは指定した値の要素を削除します。"
    },
    {
        "id": 16,
        "question": "辞書にキーと値を追加するメソッドは？",
        "code": "dic._____('b', 2)",
        "answer": "update",
        "hints": [
            "複数要素をまとめて追加可能",
            "既存キーは上書きされる"
        ],
        "explanation": "update() メソッドで辞書にキーと値を追加できます。"
    },
    {
        "id": 17,
        "question": "文字列の長さを取得する関数は？",
        "code": "length = _____('Hello')",
        "answer": "len",
        "hints": [
            "要素の数を数える関数",
            "リストや文字列に使える"
        ],
        "explanation": "len() で文字列やリストの長さを取得できます。"
    },
    {
        "id": 18,
        "question": "for文でリストの要素を順に取得する書き方は？",
        "code": "for item in _____:",
        "answer": "nums",
        "hints": [
            "リスト名を指定",
            "for in 文の基本"
        ],
        "explanation": "for item in リスト で順に要素を取得できます。"
    },
    {
        "id": 19,
        "question": "if文で条件が成り立たない場合の処理を指定するキーワードは？",
        "code": "if x > 5:\n    print(x)\n_____:\n    print('小さい')",
        "answer": "else",
        "hints": [
            "if の後に続く",
            "条件が False のときに実行"
        ],
        "explanation": "else は if 条件が False の場合に処理されます。"
    },
    {
        "id": 20,
        "question": "例外処理を行うキーワードは？",
        "code": "try:\n    1/0\n_____ ZeroDivisionError:\n    print('エラー')",
        "answer": "except",
        "hints": [
            "エラー時に処理を分ける",
            "try とセットで使う"
        ],
        "explanation": "except で指定した例外を捕まえて処理できます。"
    },
    {
        "id": 21,
        "question": "コメントを複数行書くときの方法は？",
        "code": "_____ '''これは\n複数行コメントです'''",
        "answer": "",
        "hints": [
            "Pythonでは文字列として扱う",
            "三連引用符を使う"
        ],
        "explanation": "三連引用符（''' または """）で複数行コメントとして扱えます。"
    },
    {
        "id": 22,
        "question": "リストの最後の要素を取得するインデックスは？",
        "code": "last = nums[_____]",
        "answer": "-1",
        "hints": [
            "Pythonでは負の数で末尾参照",
            "末尾は -1"
        ],
        "explanation": "nums[-1] でリストの最後の要素を取得できます。"
    },
    {
        "id": 23,
        "question": "文字列を分割するメソッドは？",
        "code": "s = 'a,b,c'\nparts = s._____(',')",
        "answer": "split",
        "hints": [
            "指定した区切り文字で分割",
            "リストに変換される"
        ],
        "explanation": "split(',') で文字列をカンマで区切り、リストにします。"
    },
    {
        "id": 24,
        "question": "文字列を結合するメソッドは？",
        "code": "parts = ['a','b','c']\ns = '-'._____('')",
        "answer": "join",
        "hints": [
            "リストを文字列にまとめる",
            "区切り文字を指定"
        ],
        "explanation": "join() を使うとリストの文字列を結合できます。"
    },
    {
        "id": 25,
        "question": "True か False の値を持つ型は？",
        "code": "flag = _____",
        "answer": "bool",
        "hints": [
            "論理値",
            "条件分岐でよく使う"
        ],
        "explanation": "bool は True または False の値を持つ型です。"
    },
    {
        "id": 26,
        "question": "文字列を整数に変換する関数は？",
        "code": "num = _____('123')",
        "answer": "int",
        "hints": [
            "数字の文字列を数値に",
            "float ではない"
        ],
        "explanation": "int('123') で文字列を整数に変換できます。"
    },
    {
        "id": 27,
        "question": "整数を文字列に変換する関数は？",
        "code": "s = _____(123)",
        "answer": "str",
        "hints": [
            "数値を文字列に変換",
            "printと組み合わせてよく使う"
        ],
        "explanation": "str(123) で数値を文字列に変換できます。"
    },
    {
        "id": 28,
        "question": "文字列を特定の文字で置換するメソッドは？",
        "code": "s = 'a-b-c'\ns._____('-', '/')",
        "answer": "replace",
        "hints": [
            "古い文字を新しい文字に置き換える",
            "文字列の変換に便利"
        ],
        "explanation": "replace('-', '/') で文字列内の '-' を '/' に置き換えます。"
    },
    {
        "id": 29,
        "question": "if文の条件が真で何も処理を行わない場合に使うキーワードは？",
        "code": "if x > 0:\n    _____",
        "answer": "pass",
        "hints": [
            "何もしない文",
            "構文を保つために使う"
        ],
        "explanation": "pass は何も処理をせずに文を終了させます。"
    },
    {
        "id": 30,
        "question": "文字列の先頭と末尾の空白を削除するメソッドは？",
        "code": "s = '  hello  '\ns = s._____()",
        "answer": "strip",
        "hints": [
            "空白を取り除く",
            "前後だけ"
        ],
        "explanation": "strip() を使うと文字列の前後の空白を削除できます。"
    }
]
