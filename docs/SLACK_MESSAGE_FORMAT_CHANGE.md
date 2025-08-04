# Slack 메시지 형식 변경 대응

## 개요

Slack에서 GitHub 커밋 링크를 보내는 방식이 변경되어, 기존 마크다운 처리 로직으로는 링크가 제대로 렌더링되지 않는 문제가 발생했습니다.

## 문제 상황

### 기존 동작
- Slack에서 GitHub 커밋 링크가 일반 마크다운 형태로 전송
- 마크다운 처리 후 정상적으로 클릭 가능한 링크로 렌더링

### 변경된 동작
- Slack에서 GitHub 커밋 링크가 백틱(`)으로 감싸진 형태로 전송
- 마크다운 처리 시 `<code>` 태그로 변환되어 링크가 작동하지 않음

### 구체적인 예시

**원본 Slack 메시지:**
```
`[8961c6b9](https://github.com/junho85/TIL/commit/8961c6b9260f3a68ebb6c42f0d6f58446aa2a0b5)` - 정원사들 시즌7
```

**마크다운 처리 후:**
```html
<p><code>[8961c6b9](https://github.com/junho85/TIL/commit/8961c6b9260f3a68ebb6c42f0d6f58446aa2a0b5)</code> - 정원사들 시즌7</p>
```

**문제점:**
- `<code>` 태그 안의 마크다운 링크가 HTML 링크로 변환되지 않음
- 커밋 해시가 텍스트로만 표시되어 클릭할 수 없음

## 해결 방법

### 1. 후처리 로직 추가

`attendance/slack_markdown.py` 파일의 `slack_markdown_to_html()` 함수에 후처리 로직을 추가했습니다.

```python
def slack_markdown_to_html(text):
    """Slack 마크다운 텍스트를 HTML로 변환"""
    if not text:
        return text
    
    md = markdown.Markdown(extensions=[SlackMarkdownExtension()])
    html = md.convert(text)
    
    # 후처리: <code> 태그 안의 GitHub 커밋 링크를 실제 링크로 변환
    # <code>[hash](url)</code> -> <code><a href="url">hash</a></code>
    html = re.sub(
        r'<code>\[([a-f0-9]+)\]\((https://github\.com/[^)]+)\)</code>',
        r'<code><a href="\2">\1</a></code>',
        html
    )
    
    return html
```

### 2. 정규식 패턴 설명

- `<code>\[([a-f0-9]+)\]\((https://github\.com/[^)]+)\)</code>`: 매칭 패턴
  - `<code>`: code 태그 시작
  - `\[([a-f0-9]+)\]`: 대괄호 안의 커밋 해시 (그룹 1)
  - `\((https://github\.com/[^)]+)\)`: 소괄호 안의 GitHub URL (그룹 2)
  - `</code>`: code 태그 종료

- `<code><a href="\2">\1</a></code>`: 치환 패턴
  - 그룹 2 (URL)를 href 속성으로, 그룹 1 (해시)을 링크 텍스트로 사용

### 3. 결과

**처리 전:**
```html
<p><code>[8961c6b9](https://github.com/junho85/TIL/commit/8961c6b9260f3a68ebb6c42f0d6f58446aa2a0b5)</code> - 정원사들 시즌7</p>
```

**처리 후:**
```html
<p><code><a href="https://github.com/junho85/TIL/commit/8961c6b9260f3a68ebb6c42f0d6f58446aa2a0b5">8961c6b9</a></code> - 정원사들 시즌7</p>
```

## 적용된 파일

- `attendance/slack_markdown.py`: 후처리 로직 추가

## 테스트 방법

1. 출석부 페이지에서 사용자별 커밋 내역 확인
2. 커밋 해시가 클릭 가능한 링크로 표시되는지 확인
3. 링크 클릭 시 해당 GitHub 커밋 페이지로 이동하는지 확인

## 향후 고려사항

- Slack 메시지 형식이 다시 변경될 가능성을 대비한 유연한 처리 로직 필요
- 다른 형태의 링크(이슈, PR 등)에도 비슷한 문제가 발생할 수 있음
- 정규식 패턴의 성능 최적화 검토