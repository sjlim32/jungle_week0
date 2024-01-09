# jungle_week0

- 새 가상환경 생성
>  python3 -m venv .venv
> (MS) py -m venv .venv

- 가상환경 활성화
<br/>*ex) Window = source 가상환경이름/Scripts/activate
> source .venv/bin/activate

- 가상환경 비활성화
> deactivate

- 가상환경 삭제
> sudo rm -rf 가상환경이름

- 이후 pip(python install package)로 실행
<br/>*ex) pip install flask


<h1> Commit 메세지 </h1>

>`예시: 'FEAT: 로그인 기능 구현'`
- **ADD**
<br/>코드, 테스트. 예제, 문서 등의 추가
- **FEAT**
<br/>새로운 기능 추가
- **FIX**
<br/>버그 수정
- **DOCS** / **UPDATE**
<br/>개정, 버전의 변경
- **STYLE**
<br/>코드 formatting, 세미콜론(;) 누락, 코드 변경이 없는 경우
- **REFECTOR**
<br/>코드 리팩터링
- **TEST**
<br/>테스트 코드, 리팩터링 테스트 코드 추가(프로덕션 코드 변경 X)
- **CHORE**
<br/>빌드 업무 수정, 패키지 매니저 수정(프로덕션 코드 변경 X)
- **DESIGN**
<br/>CSS 등 사용자 UI 디자인 변경
- **COMMENT**
<br/>필요한 주석 추가 및 변경
- **RENAME**
<br/>파일 혹은 폴더명을 수정하거나 옮기는 작업만인 경우
- **remove**
<br/>파일을 삭제하는 작업만 수행한 경우
**!BREAKING CHANGE**
<br/>커다란 API 변경의 경우
**!HOTFIX**
<br/>급하게 치명적인 버그를 고쳐야 하는 경우
