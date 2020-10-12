# 內政部 國民身分證領補換資料查詢作業 RPA

**目的**
以自動化流程方式帶入查詢資料，並以CNN模型解析驗證碼，最後送出查詢作業

## 蒐集訓練資料
1. Captcha驗證圖片來源網址：[國民身分證領補換資料查詢作業](https://www.ris.gov.tw/app/portal/3043)
2. screenshot再裁切存成Png，總共3000張
3. 使用[AntiCaptcha](http://getcaptchasolution.com/mzjmnwxcul)<sup>1</sup>協助圖片標記，人也無法辨認的資料先刪掉，人工標記不超過100張
4. 圖片前處理，彩色轉灰階，再轉黑白
5. 餵進模型前，黑白反轉，再除以255轉成01矩陣
6. 標籤資料採 one-hot label
	- 圖片內容主要由數字+英文大寫字母表示
	- 其中０、１、Ｉ、Ｌ、Ｍ、Ｏ、Ｗ不使用
	- 總共使用29種符號

## 預測模型架構
- 參考 [使用Keras基於TensorFlow和Python3.6識別高鐵驗證碼](https://github.com/gary9987/Keras-TaiwanHighSpeedRail-captcha) 最後輸出為5個Digit
- 使用Kaggle GPU環境，可以參考我的[Kaggle Notebook](https://www.kaggle.com/felisatseng/captcha-predict)<sup>2</sup>

## RPA流程
1. 使用 selenium Webdriver
2. 輸入存於config.py中的key值
3. load進訓練好的CNN模型並預測驗證碼
4. 些許偵錯機制

*備註 <sup>1</sup>：AntiCaptcha是付費服務*
*備註 <sup>2</sup>：hdf5檔案太大不能上傳，請從Kaggle下載
