CREATE TABLE bshares_sh_3yr 
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

INSERT INTO bshares_sh_3yr (date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating)
SELECT date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating
FROM 
(
    SELECT date, ticker, stock, close, high, low, open, price_change, volume, volume_usd, market_cap, cap_floating from bshares_sh_all
	WHERE date >= '2016-09-01'
)t;