# 스캔데이 왕십리점 홈페이지 프로젝트 (Scanday Homepage)

스캔데이 왕십리점의 공식 홈페이지 프로젝트입니다. 이 문서는 웹사이트의 인프라, 설정, 유지보수 및 관리 지침을 기록합니다.

---

## 1. 도메인 및 인프라 정보 (Infrastructure)

### 1.1 도메인 (Domain)
- **도메인 주소:** [scanday.kr](https://scanday.kr)
- **구매처:** **호스팅케이알 (Hosting KR)**
- **관리 상태:** `scanday.kr` 도메인이 GitHub Pages 서버로 연결되도록 DNS 설정이 완료되어 있습니다.

### 1.2 호스팅 (Hosting)
- **플랫폼:** GitHub Pages
- **저장소:** `thishw/scanday`
- **배포 방식:** `main` 브랜치에 코드를 푸시(push)하면 자동으로 라이브 서버에 반영됩니다.

---

## 2. 주요 설정 및 도구 (Configuration & Tools)

### 2.1 분석 및 트래킹 (Analytics)
- **Google Tag Manager (GTM):** 사용자 행동 분석 및 마케팅 태그 관리를 위해 설치되어 있습니다.
  - **ID:** `GTM-M69D54BW`
- **Google Analytics (GA4):** GTM을 통해 연동되어 웹사이트 방문자 데이터를 수집합니다.

### 2.2 검색 엔진 최적화 (SEO)
- **Google Search Console:** 구글 검색 결과 모니터링 및 색인 관리.
- **Naver Search Advisor:** 네이버 검색 최적화 및 사이트 맵 제출.
  - **네이버 소유권 확인 코드:** `434c06e5dd45b952ba3fe3e7b7217db9660a5e69`
- **주요 파일:**
  - `robots.txt`: 검색 로봇의 접근 권한 설정 (Naver Yeti, Googlebot 허용).
  - `sitemap.xml`: 사이트 구조를 검색 엔진에 알리기 위한 파일.
  - `CNAME`: GitHub Pages 커스텀 도메인 설정 파일 (`scanday.kr`).

---

## 3. 유지보수 가이드 (Maintenance)

### 3.1 코드 업데이트 및 배포
1. **로컬 수정:** `index.html`, `style/style.css`, `main.js` 등 수정.
2. **버전 관리:** CSS나 JS 수정 시 캐싱 문제를 방지하기 위해 `index.html`에서 파일 링크 뒤에 쿼리 스트링(예: `?v=4.1`)을 업데이트하는 것을 권장합니다.
3. **Git 푸시:**
   ```bash
   git add .
   git commit -m "feat: 가격표 업데이트 및 SEO 최적화"
   git push origin main
   ```
4. **배포 확인:** GitHub 저장소의 'Actions' 탭에서 배포 상태를 확인할 수 있습니다.

### 3.2 사이트맵(Sitemap) 및 로봇 설정
- 페이지 구조가 변경되면 `sitemap.xml`을 갱신하고 각 검색 엔진 포털(Google/Naver)에 재제출하는 것이 좋습니다.
- `robots.txt`는 모든 검색 엔진의 크롤링을 허용하도록 설정되어 있습니다.

### 3.3 가격표 및 콘텐츠 수정
- `index.html`의 `id="pricing"` 섹션에서 테이블 내용을 수정합니다.
- 영업 시간 변경 시 `index.html` 내의 **JSON-LD(구조화 데이터)** 섹션과 하단 **Reservation** 섹션을 모두 수정해야 검색 엔진 결과에 정확히 반영됩니다.

---

## 4. 관련 문서
- [MARKETING_STRATEGY.md](./MARKETING_STRATEGY.md): 브랜드 포지셔닝 및 마케팅 전략 가이드.
- `.keys/`: 배포 및 보안 관련 키 보관 (비공개 권장).

## 5. 배포 전 검증

```powershell
python scripts/generate_sitemap.py
python generate_rss.py
python scripts/audit_site.py
node --check main.js
```

- `audit_site.py`는 공개 HTML의 내부 링크·앵커, 대표 URL(canonical), 제목 구조, JSON-LD 문법, 이미지 대체텍스트, 사이트맵·RSS 동기화를 검사합니다.
- `naver_price_cards.html`은 이미지 제작용 템플릿으로 `noindex` 처리하며 사이트맵에서 제외합니다.
- HTML 변경 시 GitHub Actions가 사이트맵과 RSS를 갱신하고 검증합니다.
- 공통 메뉴는 1100px 이하에서 펼침 메뉴로 바뀝니다. 모바일 수정 시 320px, 390px, 768px 및 데스크톱에서 확인합니다.
- 확정된 대표전화·영업시간·공휴일 정책은 `project_context.md`를 기준으로 본문과 구조화 데이터를 함께 관리합니다.
- 이미지 원본을 추가하면 Pillow가 설치된 Python에서 `python scripts/optimize_images.py`로 WebP 본문용·480px 카드용 이미지를 생성합니다. 생성 파일을 커밋하므로 배포 서버에서 Pillow는 필요하지 않습니다.
- 클릭 추적은 기존 `user_interaction` 이벤트를 유지합니다. `track_action`의 `reserve_naver`, `call_store`, `view_directions`, `open_calculator`로 예약·전화·길찾기·계산기 진입을 구분합니다. 실제 예약 완료와 클릭은 별개의 지표입니다.

---

**최종 업데이트:** 2026-10-01
