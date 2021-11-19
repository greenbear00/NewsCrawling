# trobleshooting

## selenium

### 에러
#### error 1.
```
selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element
<input type="submit" id="idSIButton9" class="btn btn-block btn-primary" data-bind="
```
해결 방법:
- 해당 버튼 element을 click() 함수를 이용해 클릭하는 것이 아니라 send_keys(Keys.ENTER)를 이용해 해당 버튼 element를 클릭


#### error 2. 
```
Message: unknown error: session deleted because of page crash
from unknown error: cannot determine loading status
from tab crashed
  (Session info: headless chrome=96.0.4664.45)
```
해결방법:
- add_argument('--no-sandbox')  
- add_argument('--disable-dev-shm-usage') 