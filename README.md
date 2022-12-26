# LineChatbot - Food Finder

## 建立原因

現在的人比起以前的在家吃，通常都吃外食，但也因此延伸出了一個問題：要吃什麼？。因此，我才想設計一個line的chatbot來幫助人尋找在他們所處的縣市有什麼受到廣泛推薦的好餐廳。

## 開發環境

- windows 10
- python 3.11 (with pipenv)

## 特別技術

- beutifulsoup4
  - 爬蟲資料來源:  [愛食記](https://ifoodie.tw/) (僅作為學術研究用)

## FSM架構圖
![fsm](https://user-images.githubusercontent.com/74038554/209526491-0fe7c3ec-d7ff-4774-97fd-45de5a9eb77f.png)

- user: 輸入 "information"、"rating"、"popular" 來分別觸發機器人的功能
- information: 顯示聊天機器人的詳細資訊
- input_rating_area
- input_rating_item
- print_rating_list
- input_popular_area
- input_popular_item
- print_popular_list

## 介紹及功能展示

首先，在開始之前，還請先加入一下好友~（可以用搜尋ID的方式(記得加"@")，或者是掃下圖中的QRcode）
![image](https://user-images.githubusercontent.com/74038554/209492743-f63bf328-f19a-45a2-a893-d8d144c0fe47.png)

### 歡迎訊息(user)

在一開始進去的時候，會有一個帶有基本功能介紹的歡迎訊息。
![image](https://user-images.githubusercontent.com/74038554/209519612-a95d8921-4a1b-4fbd-bb36-251b92be8e90.png)

### information
顯示出本隻聊天機器人的餐廳資料來源和相關功能的細節說明
![image](https://user-images.githubusercontent.com/74038554/209529639-b986f428-dcf4-405e-9c90-e62270ab6b08.png)

### rating
- 輸入 "rating" 後，本支機器人會以愛食記中的 "評分高低" 來作為搜索的依據
- 使用者在進入此狀態後，我們會發送訊息，讓使用者根據我們的引導來填寫他們想要的搜索資訊，以利爬蟲結果更加符合使用者的需要。

![image](https://user-images.githubusercontent.com/74038554/209549506-70ecf254-4068-4653-b086-3f845fbb66cc.png)
![image](https://user-images.githubusercontent.com/74038554/209549535-a514c002-3048-41e4-9b30-2de7257aa914.png)

### popular
- 輸入 "popular" 後，本支機器人會以愛食記中的 "人氣高低" 來作為搜索的依據
- 使用者在進入此狀態後，基本上做的是和 "rating" 狀態差不多，根據我們的回應回復適當的訊息即可。
- 因為搜索的特徵不同的原因，所以可以發現到，在 "rating" 時的測資和此處 "popular" 中的測資是相同的，但爬蟲出來的結果是不一樣的。

![image](https://user-images.githubusercontent.com/74038554/209549964-a09efed8-736f-4b68-904a-5840eed8ab19.png)
![image](https://user-images.githubusercontent.com/74038554/209549984-ff4b237f-0e61-472d-bffd-1a35f8ee4005.png)
