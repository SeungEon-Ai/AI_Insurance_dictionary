# AI 보험용어사전

### 보험 용어를 챗봇처럼 물어보고 쉽게 확인할 수 있는 Streamlit 앱입니다.  
#### 보험 약관이나 상품 안내에서 자주 보이는 단어를 사용자가 편하게 질문하면, 내부 보험용어 DB를 먼저 찾고 필요한 경우 GPT가 설명을 보완합니다.
---
### 개발목적 

보험 콘텐츠는 관심이 있어도 용어가 어렵게 느껴지는 경우가 많습니다.  
`보험계약자`, `자동갱신계약`, `면책기간`처럼 자주 등장하지만 바로 이해하기 어려운 단어를 먼저 풀어주면, 이후 약관이나 상품 설명을 읽는 부담을 줄일 수 있습니다.

#### 이 레포는 라이나생명 프로젝트 라이나 Hub에서 첫 번째 기능으로 사용하던 `AI 보험용어사전`만 따로 분리한 버전입니다.
---
### 주요 기능 

- 보험용어 DB 기반 검색
- 자연어 질문 입력
- 예시 질문 버튼 제공
- OpenAI API 키 연결 시 GPT 보완 설명
- 로컬 테스트용 API 키 저장
- Streamlit 배포 시 secrets 기반 API 키 사용 가능
---
### 폴더 구조 

```text
.
├─ app.py
├─ requirements.txt
├─ assets/
│  └─ lina_mark_color_sharp.png
├─ features/
│  ├─ local_secrets.py
│  ├─ shared_header.py
│  └─ insurance_dictionary/
│     ├─ ai.py
│     ├─ config.py
│     ├─ data.py
│     └─ page.py
└─ outputs/
   └─ combined_insurance_terms_seed_with_life.csv
```
---
### 실행 방법 

```bash
pip install -r requirements.txt
streamlit run app.py
```

브라우저에서 아래 주소를 열면 됩니다.

```text
http://localhost:8501
```
---
### OpenAI API 키 설정 

로컬에서는 앱 화면의 `GPT API 키 입력` 영역에 키를 넣어 테스트할 수 있습니다.  
입력한 키는 `.streamlit/local_secrets.toml`에 저장되며, 이 파일은 git에 올라가지 않도록 제외했습니다.

Streamlit Cloud 등에 배포할 때는 `secrets`에 아래처럼 넣으면 됩니다.
기본적으로 설정된 모델은 GPT 4o mini 입니다.

```toml
OPENAI_API_KEY = "sk-..."
```
---
### 참고 

- 기본 검색은 DB만으로 동작합니다.
- DB는 생보협회, 손보협회, 법률 등을 크롤링하여 만들었습니다.
- GPT 연결은 설명을 자연스럽게 보완하기 위한 선택 기능입니다.
- 보험 가입 판단, 법률 판단, 실제 보장 여부 확인은 상품 약관과 보험사 안내를 기준으로 해야 합니다.
