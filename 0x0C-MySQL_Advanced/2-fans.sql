-- Rank countries by the number of metal fans
SELECT origin, SUM(fans) nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;