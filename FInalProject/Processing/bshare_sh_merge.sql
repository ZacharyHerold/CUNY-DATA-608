CREATE TABLE bshares_sh_all 
(
	date Date,
	ticker VARCHAR(10),
	stock VARCHAR(10),
	close Numeric(12, 4),
	high Numeric(12, 4),
	low Numeric(12, 4),
	open Numeric(12, 4),
	price_change VARCHAR(25),
	volume Numeric(12, 4),
	volume_usd Numeric(20, 4),
	market_cap Numeric(20, 4),
	cap_floating Numeric(20, 4)	
);

INSERT INTO bshares_sh_all (date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating)
SELECT date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating
FROM 
(
    SELECT date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900901
    union all
    select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900902
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900903
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900904
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900905
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900907
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900908
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900909
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900910
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900911
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900912
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900913
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900914
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900915
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900916
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900917
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900918
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900919
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900920
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900921
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900922
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900923
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900924
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900925
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900926
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900927
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900928
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900929
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900930
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900932
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900933
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900934
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900936
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900937
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900938
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900939
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900940
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900941
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900942
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900943
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900945
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900946
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900947
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900948
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900951
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900952
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900953
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900955
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900956
    union all
	select date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from sh900957
)t;