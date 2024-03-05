-- Задание 2
-- Название и продолжительность самого длительного трека.
SELECT track_name, track_time
  FROM tracks
 WHERE track_time = (
    SELECT MAX(track_time)
    FROM tracks
 );
/*
  track_name   | track_time
---------------+------------
 Кончится лето | 00:05:55
(1 row)
*/

-- Название треков, продолжительность которых не менее 3,5 минут.
SELECT track_name, track_time
  FROM tracks
 WHERE track_time >= '00:03:30'
 ORDER BY track_time DESC
 LIMIT 5;
/*
    track_name     | track_time
-------------------+------------
 Кончится лето     | 00:05:55
 Красно-жёлтые дни | 00:05:49
 Песня без слов    | 00:05:06
 Нам с тобой       | 00:04:49
 This Loss         | 00:04:41
(5 rows)
*/

-- Названия сборников, вышедших в период с 2018 по 2020 год включительно.
SELECT collection_name
  FROM collections
 WHERE release_year BETWEEN 2018 AND 2020;
/*
 collection_name
-----------------
 Потяжелее
 Pop
(2 rows)
*/

-- Исполнители, чьё имя состоит из одного слова.
SELECT artist_name
  FROM artist
 WHERE artist_name NOT LIKE '% %'
 ORDER BY artist_name
 LIMIT 5;
/*
 artist_name
-------------
 AMATORY
 AQUA
 Gorillaz
 KORN
 Zaz
(5 rows)
*/

-- название треков, которые содержат слово “мой”/“my”.
SELECT track_name
  FROM tracks
 WHERE track_name ILIKE '%my%' OR track_name ILIKE '%мой%';
/*
track_name       |
-----------------+
Fake My Own Death|
Kill Myself      |
My Medication    |
My Confession    |*/

-- Задание 3
-- Количество исполнителей в каждом жанре.
SELECT genre_name, COUNT(*) AS "Количество исполнителей"
  FROM genre
 INNER JOIN genre_artist USING(genre_id)
 INNER JOIN artist USING(artist_id)
 GROUP BY genre_name;
/*
 genre_name  | Количество исполнителей
-------------+-------------------------
 ALTERNATIVE |                       3
 PUNK        |                       3
 ROCK        |                       4
 POP         |                       4
(4 rows)
*/

-- Количество треков, вошедших в альбомы 2019–2020 годов.
SELECT COUNT(*) AS "Количество треков"
  FROM tracks
 INNER JOIN album USING(album_id)
 WHERE album.release_year BETWEEN 2019 AND 2020;
/*
 Количество треков
-------------------
                13
(1 row)
*/

-- Средняя продолжительность треков по каждому альбому.
SELECT album_name, AVG(track_time) AS "Средняя продолжительность"
  FROM tracks
 INNER JOIN album USING(album_id)
 GROUP BY album_name
 ORDER BY "Средняя продолжительность" DESC
 LIMIT 5;
/*
       album_name       | Средняя продолжительность
------------------------+---------------------------
 Черный альбом          | 00:05:31
 Звезда по имени Солнце | 00:04:23
 The Nothing            | 00:04:13.5
 Aquarius               | 00:04:12
 Demon Days             | 00:03:48.666667
(5 rows)
*/

-- Все исполнители, которые не выпустили альбомы в 2020 году.
SELECT artist_name
  FROM artist
 WHERE artist_name NOT IN (
    SELECT artist_name
      FROM artist
     INNER JOIN album_artist USING(artist_id)
     INNER JOIN album USING(album_id)
     WHERE release_year = 2020);
/*
 artist_name
--------------
 SUM 41
 Король и Шут
 Элизиум
 Gorillaz
 КИНО
 Zaz
 Zivert
 AQUA
 Papa Roach
 KORN
 AMATORY
(11 rows)
*/

-- Названия сборников, в которых присутствует конкретный исполнитель (выберите его сами).
SELECT DISTINCT(collection_name)
  FROM collections
 INNER JOIN track_collections USING(collection_id)
 INNER JOIN tracks USING(track_id)
 INNER JOIN album USING(album_id)
 INNER JOIN album_artist USING(album_id)
 INNER JOIN artist USING(artist_id)
 WHERE artist_name = 'KORN';
/*
 collection_name
-----------------
 Потяжелее
(1 row)
*/

-- Задание 4(необязательное)
-- Названия альбомов, в которых присутствуют исполнители более чем одного жанра.
SELECT album_name, artist_name
  FROM album
 INNER JOIN album_artist USING(album_id)
 INNER JOIN artist USING(artist_id)
 WHERE artist_id IN (
    SELECT artist_id
      FROM artist
     INNER JOIN genre_artist USING(artist_id)
     INNER JOIN genre USING(genre_id)
     GROUP BY artist_id
     HAVING COUNT(*) > 1
 );
/*
     album_name      | artist_name
---------------------+--------------
 Герои и Злодеи      | Король и Шут
 Как в старой сказке | Король и Шут
 Все острова         | Элизиум
 Космос              | Элизиум
(4 rows)
*/

-- Наименования треков, которые не входят в сборники.
SELECT track_name
  FROM tracks
 WHERE track_id NOT IN (
    SELECT track_id
      FROM track_collections
     INNER JOIN collections USING(collection_id)
)
 LIMIT 5;-- (43 rows)
/*
      track_name
-----------------------
 Goddamn Im Dead Again
 Fake My Own Death
 Turning Away
 Out For Blood
 The New Sensation
(5 rows)
*/

-- Исполнитель или исполнители, написавшие самый короткий по продолжительности трек, — теоретически таких треков может быть несколько.
SELECT artist_id, artist_name, track_id, track_name, track_time
  FROM artist
 INNER JOIN album_artist USING(artist_id)
 INNER JOIN album USING(album_id)
 INNER JOIN tracks USING(album_id)
 WHERE track_id IN (
    SELECT track_id
      FROM tracks
     WHERE track_time = (
        SELECT MIN(track_time)
          FROM tracks)
);
/*
 artist_id | artist_name | track_id | track_name | track_time
-----------+-------------+----------+------------+------------
         3 | Элизиум     |       18 | Солнце     | 00:02:15
(1 row)
*/

-- Названия альбомов, содержащих наименьшее количество треков.

SELECT album_name, COUNT(track_id) AS "track_count"
  FROM album
 INNER JOIN tracks USING(album_id)
 GROUP BY album_name
HAVING COUNT(*) = (
    SELECT MIN(inn)
	  FROM (
        SELECT COUNT(album_name) AS inn
	      FROM album
	     INNER JOIN tracks USING(album_id)
	     GROUP BY album_name) AS inn);
/*
    album_name     | track_count
-------------------+-------------
 Who Do You Trust? |           1
(1 row)
*/