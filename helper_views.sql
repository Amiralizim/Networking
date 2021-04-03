CREATE VIEW private_ips AS 
SELECT srcIP, srcPort, dstIP, dstPort 
FROM Links 
WHERE
((CAST(SUBSTRING_INDEX(srcIP, ".", -4) AS int) = 10) OR
(CAST(SUBSTRING_INDEX(srcIP, ".", -4) AS int) = 192 AND CAST(SUBSTRING_INDEX(srcIP, ".", -3) AS int) = 168) OR
(CAST(SUBSTRING_INDEX(srcIP, ".", -4) AS int) = 172 AND 16 < CAST(SUBSTRING_INDEX(srcIP, ".", -3) AS int) < 31))
GROUP BY srcIP, srcPort, dstIP, dstPort;

CREATE VIEW public_ips AS 
SELECT srcIP, srcPort, dstIP, dstPort 
FROM Links 
WHERE
NOT ((CAST(SUBSTRING_INDEX(srcIP, ".", -4) AS int) = 10) OR
(CAST(SUBSTRING_INDEX(srcIP, ".", -4) AS int) = 192 AND CAST(SUBSTRING_INDEX(srcIP, ".", -3) AS int) = 168) OR
(CAST(SUBSTRING_INDEX(srcIP, ".", -4) AS int) = 172 AND 16 < CAST(SUBSTRING_INDEX(srcIP, ".", -3) AS int) < 31))
GROUP BY srcIP, srcPort, dstIP, dstPort;
