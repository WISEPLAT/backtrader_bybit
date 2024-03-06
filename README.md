# backtrader_bybit
Bybit API integration with [Backtrader](https://github.com/WISEPLAT/backtrader).

With this integration you can do:
 - Backtesting your strategy on historical data from the exchange [Bybit](https://www.bybit.com/invite?ref=KXLXXE%230 ) + [Backtrader](https://github.com/WISEPLAT/backtrader )  // Backtesting 
 - Launch trading systems for automatic trading on the exchange [Bybit](https://www.bybit.com/invite?ref=KXLXXE%230 ) + [Backtrader](https://github.com/WISEPLAT/backtrader ) // Live trading
 - Download historical data for cryptocurrencies from the exchange [Bybit](https://www.bybit.com/invite?ref=KXLXXE%230)

For API connection we are using library [pybit](https://github.com/bybit-exchange/pybit).

**You can say Thanks:**

USDT (Tron TRC20): TEHaXZX7KLjAm4eLWdf4VKfsqRUQpv8fTT

BTC (Bitcoin BTC): 1ENhx1HUMJZjGAfYaT1vfsqwKHgVkqwX1D

ETH (Ethereum ERC20): 0xfd546640c911ba90d1409a4fbbb4322ae73e7814

## Installation
1) The simplest way:
```shell
pip install backtrader_bybit
```
or
```shell
git clone https://github.com/WISEPLAT/backtrader_bybit
```
or
```shell
pip install git+https://github.com/WISEPLAT/backtrader_bybit.git
```

2) Please use backtrader from my repository (as your can push your commits in it). Install it:
```shell
pip install git+https://github.com/WISEPLAT/backtrader.git
```
-- Can I use your bybit interface with original backtrader?

-- Yes, you can use original backtrader, as the author of original backtrader had approved all my changes. 

Here is the link: [mementum/backtrader#472](https://github.com/mementum/backtrader/pull/472)

3) We have some dependencies, you need to install them: 
```shell
pip install pybit pycryptodome backtrader pandas matplotlib
```

or

```shell
pip install -r requirements.txt
```

### Getting started
To make it easier to figure out how everything works, many examples have been made in the folders **DataExamplesBybit** and **StrategyExamplesBybit**.

Before running the example, you need to get your API key, Secret key and Type of Account, and put them in the file **ConfigBybit\Config.py:**

```python
# content of ConfigBybit\Config.py 
class Config:
    BYBIT_API_KEY = "YOUR_API_KEY"
    BYBIT_API_SECRET = "YOUR_SECRET_KEY"
    BYBIT_ACCOUNT_TYPE = "UNIFIED"  # UNIFIED or CONTRACT
```

#### How to get a Bybit API token:
1. Register your account on [Bybit](https://www.bybit.com/invite?ref=KXLXXE%230 )
2. Go to ["Profile" -> "API Management"](https://www.bybit.com/app/user/api-management?ref=KXLXXE%230 ) 
3. Then push the button "Create New Key" and select "System generated"
4. In "API Key restrictions" enable "Read-Write" and in "Unified Trading"->"SPOT" enable "Trade"
5. Copy and paste to the file **ConfigBybit\Config.py ** received **"API key"** and **"Secret key"**

#### Now you can run examples

The **DataExamplesBybit** folder contains the code of examples for working with exchange data via the [Bybit](https://www.bybit.com/invite?ref=KXLXXE%230 ) API.

* **01 - Symbol.py** - trading strategy for obtaining historical and "live" data of one ticker for one timeframe
* **02 - Symbol data to DF.py** - export to csv file of historical data of one ticker for one timeframe
* **03 - Symbols.py** - trading strategy for multiple tickers on the same timeframe
* **04 - Resample.py** - trading strategy for obtaining data from one ticker for different timeframes by converting a smaller timeframe into a larger one
* **05 - Replay.py** - launching a trading strategy on a smaller timeframe, with processing on a larger one and displaying a larger interval chart
* **06 - Rollover.py** - launch of a trading strategy based on gluing data from a file with historical data and the last downloaded history from the broker
* **08 - Timeframes.py** - trading strategy is running on different timeframes.
* **09 - Get Asset Info - through client.py** - getting info about asset: balance, lot size, min price step, min value to buy and etc.
* **Strategy.py** - An example of a trading strategy that only outputs data of the OHLCV for ticker/tickers

The **StrategyExamplesBybit** folder contains the code of sample strategies.

* **01 - Live Trade - Just Buy and Sell.py** - An example of a live trading strategy for ETH ticker on the base USDT ticker.
  * The strategy shows how to Buy at Market or Limit order and how to Cancel order.
  * Example of placing and cancel orders on the Bybit exchange.
    * Please be aware! This is Live order - if market has a big change down in value of price more than 5% - the order will be completed....
    * Please be aware! For Market order - it will be completed!
    * **Do not forget to cancel the submitted orders from the exchange after the test!**

* **01 - Live Trade.py** - An example of a live trading strategy for two BTC and ETH tickers on the base USDT ticker.
  * The strategy shows how to apply indicators (SMA, RSI) to several tickers at the same time.
  * Example of placing and cancel orders on the Bybit exchange.
    * Please be aware! This is Live order - if market has a big change down in value of price more than 5% - the order will be completed.... 
    * **Do not forget to cancel the submitted orders from the exchange after the test!**


* **02 - Live Trade MultiPortfolio.py** - An example of a live trading strategy for a set of tickers that can be transferred to the strategy in a list (BTC, ETH, BNB) on the base USDT ticker.
  * The strategy shows how to apply indicators (SMA, RSI) to several tickers at the same time.
  * Example of placing and cancel orders on the Bybit exchange.
    * Please be aware! This is Live order - if market has a big change down in value of price more than 5% - the order will be completed.... 
    * **Do not forget to cancel the submitted orders from the exchange after the test!**


* **03 - Live Trade ETH.py** - An example of a live trading strategy for two BNB and XMR tickers on the basic ETH ticker.
  * The strategy shows how to apply indicators (SMA, RSI) to several tickers at the same time.
  * Example of placing and cancel orders on the Bybit exchange.
    * Please be aware! This is Live order - if market has a big change down in value of price more than 5% - the order will be completed.... 
    * **Do not forget to cancel the submitted orders from the exchange after the test!**


* **04 - Offline Backtest.py** - An example of a trading strategy on a historical data - not live mode - for two BTC and ETH tickers on the base USDT ticker.
  * The strategy shows how to apply indicators (SMA, RSI) to several tickers at the same time.
    * Not a live mode - for testing strategies without sending orders to the exchange!


* **05 - Offline Backtest MultiPortfolio.py** - An example of a trading strategy on a historical data - not live mode - for a set of tickers that can be transferred to the strategy in a list (BTC, ETH, BNB) on the base USDT ticker.
  * The strategy shows how to apply indicators (SMA, RSI) to several tickers at the same time.
    * Not a live mode - for testing strategies without sending orders to the exchange!


* **06 - Live Trade Just Buy and Close by Market.py** - An example of a live trading strategy for ETH ticker on the base USDT ticker.
  * The strategy shows how to buy by close price and sell by market a little value of ETH after 3 bars.
  * Example of placing orders on the Bybit exchange.
    * **Do not forget to cancel the submitted orders from the exchange after the test!**


* **07 - Offline Backtest Indicators.py** - An example of a trading strategy for a history test using SMA and RSI indicators - not live mode - for two BTC and ETH tickers on the base USDT ticker.
  * The strategy shows how to apply indicators (SMA, RSI) to several tickers at the same time.
    * generates 177% of revenue at the time of video recording))
    * Non-live mode - for testing strategies without sending orders to the exchange!

## Thanks
- backtrader: Very simple and cool library!
- [pybit](https://github.com/bybit-exchange/pybit): For creating Bybit API wrapper, shortening a lot of work.

## License
[MIT](https://choosealicense.com/licenses/mit)

## Important
Error correction, revision and development of the library is carried out by the author and the community!

**Push your commits!**

## Terms of Use
The backtrader_bybit library, which allows you to integrate Backtrader and Bybit API, is the **Program** created solely for the convenience of work.
When using the **Program**, the User is obliged to comply with the provisions of the current legislation of his country.
Using the **Program** are offered on an "AS IS" basis. No guarantees, either oral or written, are attached and are not provided.
The author and the community does not guarantee that all errors of the **Program** have been eliminated, respectively, the author and the community do not bear any responsibility for
the consequences of using the **Program**, including, but not limited to, any damage to equipment, computers, mobile devices,
User software caused by or related to the use of the **Program**, as well as for any financial losses
incurred by the User as a result of using the **Program**.
No one is responsible for data loss, losses, damages, including accidental or indirect, lost profits, loss of revenue or any other losses
related to the use of the **Program**.

The **Program** is distributed under the terms of the [MIT](https://choosealicense.com/licenses/mit ) license.

## Star History

Please put a Star 🌟 for this code

[![Star History Chart](https://api.star-history.com/svg?repos=WISEPLAT/backtrader_bybit&type=Timeline)](https://star-history.com/#WISEPLAT/backtrader_bybit&Timeline)

Пожалуйста поставьте Звезду 🌟 этому коду

==========================================================================

# backtrader_bybit

Интеграция Bybit API с [Backtrader](https://github.com/WISEPLAT/backtrader ).

С помощью этой интеграции вы можете делать:
- Тестирование вашей стратегии на исторических данных с биржи [Bybit](https://www.bybit.com/invite?ref=KXLXXE%230 ) + [Backtrader](https://github.com/WISEPLAT/backtrader )
- Запускать торговые системы для автоматической торговли на бирже [Bybit](https://www.bybit.com/invite?ref=KXLXXE%230 ) + [Backtrader](https://github.com/WISEPLAT/backtrader ) 
- Загружать исторические данные по криптовалютам с биржи [Bybit](https://www.bybit.com/invite?ref=KXLXXE%230 )

Для подключения к API мы используем библиотеку [pybit](https://github.com/bybit-exchange/pybit ).

**Можно сказать Спасибо:**

USDT (Tron TRC20): TEHaXZX7KLjAm4eLWdf4VKfsqRUQpv8fTT

BTC (Bitcoin BTC): 1ENhx1HUMJZjGAfYaT1vfsqwKHgVkqwX1D

ETH (Ethereum ERC20): 0xfd546640c911ba90d1409a4fbbb4322ae73e7814


## Установка
1) Самый простой способ:
```shell
pip install backtrader_bybit
```
или
```shell
git clone https://github.com/WISEPLAT/backtrader_bybit
```
или
```shell
pip install git+https://github.com/WISEPLAT/backtrader_bybit.git
```

2) Пожалуйста, используйте backtrader из моего репозитория (так как вы можете размещать в нем свои коммиты). Установите его:
```shell
pip install git+https://github.com/WISEPLAT/backtrader.git
```
-- Могу ли я использовать ваш интерфейс bybit с оригинальным backtrader?

-- Да, вы можете использовать оригинальный backtrader, так как автор оригинального backtrader одобрил все мои изменения.

Вот ссылка: [mementum/backtrader#472](https://github.com/mementum/backtrader/pull/472)

3) У нас есть некоторые зависимости, вам нужно их установить:
```shell
pip install pybit pycryptodome backtrader pandas matplotlib
```

или

```shell
pip install -r requirements.txt
```

### Начало работы
Чтобы было легче разобраться как всё работает, сделано множество примеров в папках **DataExamplesBybit_ru** и **StrategyExamplesBybit_ru**.

Перед запуском примера, необходимо получить свой API ключ, Secret ключ и Тиа аккаунта, и прописать их в файле **ConfigBybit\Config.py:**

```python
# content of ConfigBybit\Config.py 
class Config:
    BYBIT_API_KEY = "YOUR_API_KEY"
    BYBIT_API_SECRET = "YOUR_SECRET_KEY"
    BYBIT_ACCOUNT_TYPE = "UNIFIED"  # UNIFIED or CONTRACT
```

####  Как получить токен Bybit API:
1. Зарегистрируйте свой аккаунт на [Bybit](https://www.bybit.com/invite?ref=KXLXXE%230 )
2. Перейдите в ["Профиль" -> """Управление API"](https://www.bybit.com/app/user/api-management?ref=KXLXXE%230 )
3. Затем нажмите кнопку "Создать Новый Ключ" и выберите "Сгенерированный системой".
4. В разделе "Разрешения API ключа" включите ""Чтение и запись" и в "Единый торговый аккаунт"->"СПОТ" включите "Торговать".
5. Скопируйте и вставьте в файл **ConfigBybit\Config.py** полученные **"Ключ API"** и **"Секретный ключ"**

#### Теперь можно запускать примеры

В папке **DataExamplesBybit_ru** находится код примеров по работе с биржевыми данными через API интерфейс [Bybit](https://www.bybit.com/invite?ref=KXLXXE%230 ).

* **01 - Symbol.py** - торговая стратегия для получения исторических и "живых" данных одного тикера по одному таймфрейму
* **02 - Symbol data to DF.py** - экспорт в csv файл исторических данных одного тикера по одному таймфрейму
* **03 - Symbols.py** - торговая стратегия для нескольких тикеров по одному таймфрейму
* **04 - Resample.py** - торговая стратегия для получения данных одного тикера по разным таймфреймам методом конвертации меньшего таймфрейма в больший
* **05 - Replay.py** - запуск торговой стратегии на меньшем таймфрейме, с обработкой на большем и выводом графика большего интервала
* **06 - Rollover.py** - запуск торговой стратегии на склейке данных из файла с историческими данными и последней загруженной истории с брокера
* **08 - Timeframes.py** - торговая стратегия для одного тикера по разным таймфреймам
* **09 - Get Asset Info - through client.py** - получение информации об активе: баланс, размер лота, минимальный шаг цены, минимальная стоимость покупки и т.д.
* **Strategy.py** - Пример торговой стратегии, которая только выводит данные по тикеру/тикерам OHLCV

В папке **StrategyExamplesBybit_ru** находится код примеров стратегий.  

* **01 - Live Trade - Just Buy and Sell.py** - Пример торговой стратегии в live режиме для ETH на базовом тикере USDT. 
  * В стратегии показано как выставлять Ордер по Рынку и Лимитный ордер и как отменять ордер. 
  * Пример выставления заявок на биржу Bybit и их снятие.
    * Пожалуйста, имейте в виду! Это live режим - если на рынке произойдет значительное изменение цены в сторону понижения более чем на 5% - ордер может быть выполнен....
    * Пожалуйста, имейте в виду! Для ордера по Рынку - он будет выполнен....
    * **Не забудьте после теста снять с биржи выставленные заявки!**

* **01 - Live Trade.py** - Пример торговой стратегии в live режиме для двух тикеров BTC и ETH на базовом тикере USDT. 
  * В стратегии показано как применять индикаторы (SMA, RSI) к нескольким тикерам одновременно. 
  * Пример выставления заявок на биржу Bybit и их снятие.
    * Пожалуйста, имейте в виду! Это live режим - если на рынке произойдет значительное изменение цены в сторону понижения более чем на 5% - ордер может быть выполнен.... 
    * **Не забудьте после теста снять с биржи выставленные заявки!**


* **02 - Live Trade MultiPortfolio.py** - Пример торговой стратегии в live режиме для множества тикеров, которые можно передавать в стратегию списком (BTC, ETH, BNB) на базовом тикере USDT. 
  * В стратегии показано как применять индикаторы (SMA, RSI) к нескольким тикерам одновременно. 
  * Пример выставления заявок на биржу Bybit и их снятие.
    * Пожалуйста, имейте в виду! Это live режим - если на рынке произойдет значительное изменение цены в сторону понижения более чем на 5% - ордер может быть выполнен....
    * **Не забудьте после теста снять с биржи выставленные заявки!**


* **03 - Live Trade ETH.py** - Пример торговой стратегии в live режиме для двух тикеров BNB и XMR на базовом тикере ETH. 
  * В стратегии показано как применять индикаторы (SMA, RSI) к нескольким тикерам одновременно. 
  * Пример выставления заявок на биржу Bybit и их снятие.
    * Пожалуйста, имейте в виду! Это live режим - если на рынке произойдет значительное изменение цены в сторону понижения более чем на 5% - ордер может быть выполнен....
    * **Не забудьте после теста снять с биржи выставленные заявки!**


* **04 - Offline Backtest.py** - Пример торговой стратегии для теста на истории - не live режим - для двух тикеров BTC и ETH на базовом тикере USDT. 
  * В стратегии показано как применять индикаторы (SMA, RSI) к нескольким тикерам одновременно.
    * Не live режим - для тестирования стратегий без отправки заявок на биржу!


* **05 - Offline Backtest MultiPortfolio.py** - Пример торговой стратегии для теста на истории - не live режим - для множества тикеров, которые можно передавать в стратегию списком (BTC, ETH, BNB) на базовом тикере USDT. 
  * В стратегии показано как применять индикаторы (SMA, RSI) к нескольким тикерам одновременно.
    * Не live режим - для тестирования стратегий без отправки заявок на биржу!


* **06 - Live Trade Just Buy and Close by Market.py** - Пример торговой стратегии в live для тикера ETH на базовом тикере USDT.
  * Стратегия показывает, как покупать по цене закрытия и продавать по рыночной небольшое количество ETH через 3 бара.
  * Пример размещения ордеров на бирже Bybit.
    * **Не забудьте отменить выставленные ордера с биржи после тестирования!**


* **07 - Offline Backtest Indicators.py** - Пример торговой стратегии для теста на истории с использованием индикаторов SMA и RSI - не live режим - для двух тикеров BTC и ETH на базовом тикере USDT. 
  * В стратегии показано как применять индикаторы (SMA, RSI) к нескольким тикерам одновременно.
    * генерит 177% дохода на момент записи видео )) 
    * Не live режим - для тестирования стратегий без отправки заявок на биржу!

## Спасибо
- backtrader: очень простая и классная библиотека!
- [pybit](https://github.com/bybit-exchange/pybit ): Для создания оболочки Bybit API, сокращающей большую часть работы.

## Важно
Исправление ошибок, доработка и развитие библиотеки осуществляется автором и сообществом!

**Пушьте ваши коммиты!** 

# Условия использования
Библиотека backtrader_bybit позволяющая делать интеграцию Backtrader и Bybit API - это **Программа** созданная исключительно для удобства работы.
При использовании **Программы** Пользователь обязан соблюдать положения действующего законодательства Российской Федерации или своей страны.
Использование **Программы** предлагается по принципу «Как есть» («AS IS»). Никаких гарантий, как устных, так и письменных не прилагается и не предусматривается.
Автор и сообщество не дает гарантии, что все ошибки **Программы** были устранены, соответственно автор и сообщество не несет никакой ответственности за
последствия использования **Программы**, включая, но, не ограничиваясь любым ущербом оборудованию, компьютерам, мобильным устройствам, 
программному обеспечению Пользователя вызванным или связанным с использованием **Программы**, а также за любые финансовые потери,
понесенные Пользователем в результате использования **Программы**.
Никто не ответственен за потерю данных, убытки, ущерб, включаю случайный или косвенный, упущенную выгоду, потерю доходов или любые другие потери,
связанные с использованием **Программы**.

**Программа** распространяется на условиях лицензии [MIT](https://choosealicense.com/licenses/mit).
