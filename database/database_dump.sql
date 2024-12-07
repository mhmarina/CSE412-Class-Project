--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2 (Debian 17.2-1.pgdg120+1)
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: answers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.answers (
    a_answerid character(1) NOT NULL,
    a_questionid integer NOT NULL,
    a_answertext character varying(255) NOT NULL,
    a_iscorrect boolean
);


ALTER TABLE public.answers OWNER TO postgres;

--
-- Name: asked; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.asked (
    as_sessionid bigint NOT NULL,
    as_questionid integer NOT NULL,
    as_answeredby bigint NOT NULL,
    as_answer character(1),
    as_iscorrect boolean
);


ALTER TABLE public.asked OWNER TO postgres;

--
-- Name: plays; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plays (
    p_userid bigint NOT NULL,
    p_sessionid bigint NOT NULL,
    p_score integer
);


ALTER TABLE public.plays OWNER TO postgres;

--
-- Name: questions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.questions (
    q_questionid integer NOT NULL,
    q_hint character varying(255),
    q_category character varying(255),
    q_questiontext character varying(255) NOT NULL
);


ALTER TABLE public.questions OWNER TO postgres;

--
-- Name: triviasession; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.triviasession (
    t_sessionid bigint NOT NULL,
    t_starttime timestamp without time zone,
    t_stoptime timestamp without time zone
);


ALTER TABLE public.triviasession OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    u_userid bigint NOT NULL,
    u_totalscore integer,
    u_username character varying(32) NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: answers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.answers (a_answerid, a_questionid, a_answertext, a_iscorrect) FROM stdin;
a	1	Middle Ages	f
b	1	The Industrial Revolution	t
c	1	The Bronze Age	f
a	2	Phoenix	f
b	2	Salt Lake City	f
c	2	Kansas City	t
a	3	Mosquitoes	t
b	3	Killer Sharks	f
c	3	Humans	f
a	4	DeathBerries	f
b	4	Nightlock	t
c	4	Apples	f
a	11	2	f
b	11	3	t
c	11	4	f
a	12	Elephant	t
b	12	Hippopotamus	f
c	12	Tortoise	f
a	13	2,000lbs	f
b	13	10,000lbs	f
c	13	6,000lbs	t
a	14	Mottled Duck	f
b	14	American Woodcock	f
c	14	Arctic Tern	t
a	15	pink	f
b	15	black	t
c	15	white	f
a	16	China	f
b	16	Iceland	t
c	16	England	f
a	17	38 minutes	t
b	17	23 minutes	f
c	17	52 minutes	f
a	18	776	f
b	18	887	t
c	18	693	f
a	19	60 million	f
b	19	90 million	f
c	19	75 million	t
a	20	207 BC	f
b	20	220 AD	f
c	20	1878	t
a	21	Asia	f
b	21	South America	f
c	21	Africa	t
a	22	Chimborazo	t
b	22	Everest	f
c	22	K2	f
a	23	North America	f
b	23	Antarctica	t
c	23	Africa	f
a	24	Dead Sea	t
b	24	Death Valley	f
c	24	Purgatory	f
a	25	Indonesia	f
b	25	Philippines	f
c	25	Sweden	t
a	26	12.1cm	f
b	26	7.5cm	t
c	26	10.2cm	f
a	27	56	f
b	27	82	f
c	27	33	t
a	28	1875	f
b	28	1963	t
c	28	1632	f
a	29	Jerry West	t
b	29	Wilt Chamberlain	f
c	29	Michael Jordan	f
a	30	playing card	f
b	30	cabbage leaf	t
c	30	family portrait	f
a	31	Ireland	f
b	31	United States	f
c	31	Japan	t
a	32	1902	f
b	32	1796	f
c	32	1888	t
a	33	Carlos	t
b	33	Charles	f
c	33	William	f
a	34	Abigail Housemouse	f
b	34	Anna Pocketmouse	f
c	34	Amelia Fieldmouse	t
a	35	The Nutcracker	t
b	35	Swan Lake	f
c	35	Romeo and Juliet	f
a	36	3 hours	f
b	36	39 minutes	t
c	36	53 seconds	f
a	37	30	f
b	37	50	f
c	37	90	t
a	38	Sargasso Sea	t
b	38	Black Sea	f
c	38	Arabian Sea	f
a	39	5mm	t
b	39	1mm	f
c	39	3mm	f
a	40	United States	f
b	40	China	f
c	40	Papua New Guinea	t
a	41	112	f
b	41	76	f
c	41	108	t
a	42	93ft	f
b	42	89ft	t
c	42	78ft	f
a	43	Basketball	f
b	43	Soccer	f
c	43	Baseball	t
a	44	Golf	t
b	44	Soccer	f
c	44	Darts	f
a	45	Crushed can	f
b	45	Frozen cow poop	t
c	45	Sliced fruit	f
a	46	Deadpool	f
b	46	Fight Club	t
c	46	The Social Network	f
a	47	30,000	t
b	47	10,000	f
c	47	50,000	f
a	48	Sexual Healing	f
b	48	Cold Blooded	f
c	48	Billie Jean	t
a	49	Rudolph	f
b	49	King Kong	t
c	49	Viking	f
a	50	Thomas Pennyfeather	f
b	50	Thomas Mapother	t
c	50	Thomas Wormwell	f
a	51	2 years	f
b	51	4 years	t
c	51	6 years	f
a	52	1600	t
b	52	106,000	f
c	52	57,000	f
a	53	1812	f
b	53	1884	f
c	53	1797	t
a	54	40	t
b	54	0	f
c	54	70	f
a	55	1910	f
b	55	1903	t
c	55	1912	f
a	56	1 week	t
b	56	1 day	f
c	56	1 hour	f
a	57	15	f
b	57	5	f
c	57	10	t
a	58	2	f
b	58	4	f
c	58	9	t
a	59	White	f
b	59	Pink	t
c	59	Yellow	f
a	60	Giant squid	t
b	60	Blue whale	f
c	60	African elephant	f
\.


--
-- Data for Name: asked; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.asked (as_sessionid, as_questionid, as_answeredby, as_answer, as_iscorrect) FROM stdin;
\.


--
-- Data for Name: plays; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.plays (p_userid, p_sessionid, p_score) FROM stdin;
\.


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.questions (q_questionid, q_hint, q_category, q_questiontext) FROM stdin;
1	\N	History	Which era marked a switch from agricultural practices to industrial practices?
2	\N	Geography	What United States city is known as "The City of Fountains?"
3	\N	Nature	What is the deadliest creature in the world?
4	\N	Entertainment	What do Katniss and Peeta attempt to poison themselves with in The Hunger Games?
11	\N	Nature	How many hearts does an octopus have?
12	\N	Nature	What is the only animal that cannot jump?
13	\N	Nature	How much does a blue whale tongue weigh?
14	\N	Nature	What bird has the longest migration?
15	\N	Nature	What color is polar bear skin?
16	\N	History	What country has the world's oldest parliament?
17	\N	History	What was the length of the shortest war in history?
18	\N	History	How many giant head statues are on Easter Island?
19	\N	History	How many people died of bubonic plague during the Middle Ages?
20	\N	History	What year was the Great Wall of China completed?
21	\N	Geography	What continent can be found in all four hemispheres?
22	\N	Geography	What mountain is closest to space?
23	\N	Geography	What continent has the largest desert?
24	\N	Geography	What is the lowest natural point on Earth?
25	\N	Geography	What country has the most islands?
26	\N	Geography	How much closer does Hawaii get to Alaska every year?
27	\N	Sports	With 8000+ sports played around the world, how many are included in the Olympics?
28	\N	Sports	How many assists does Wayne Gretzky have?
29	\N	Sports	Who is the silhouette on the official NBA logo?
30	\N	Sports	What did Babe Ruth wear under his cap for good luck?
31	\N	Sports	What country has the largest bowling alley?
32	\N	Entertainment	What year was the first moving picture?
33	\N	Entertainment	What is Chuck Norris's first name?
34	\N	Entertainment	Who is Mickey Mouse's sister?
35	\N	Entertainment	What is the most popular ballet in the world?
36	\N	Entertainment	How often is a new porn film made in the US?
37	\N	Geography	What percentage of the population lives in the northern hemisphere?
38	\N	Geography	What is the only sea with no coast?
39	\N	Geography	How much taller do the Himalayas get every year?
40	\N	Geography	What country is the most linguistically diverse in the world?
41	\N	Sports	How many stitches are on a baseball?
42	\N	Sports	What is the length of the longest successful shot in NBA history?
43	\N	Sports	What sport popularized identifying players by their jersey number?
44	\N	Sports	What was the first sport played on the moon?
45	\N	Sports	What was used as the first ever puck in a hockey game?
46	\N	Entertainment	What movie has a Starbucks cup in every scene?
47	\N	Entertainment	How many commercials does the average child see each year?
48	\N	Entertainment	What was the first music video to air on MTV by a black artist?
49	\N	Entertainment	What was Hitler's favorite movie?
50	\N	Entertainment	What is Tom Cruise's real name?
51	\N	History	Prior to Covid19, what was the shortest record for a vaccine to be developed and licensed?
52	\N	History	Napoleon took 187,600 horses with his army as he rode into Russia in 1812, how many came back?
53	\N	History	When was the first skyscraper built?
54	\N	History	What percentage of English brides in 1800 were pregnant at the altar?
55	\N	History	When was the first powered flight by the Wright Brothers?
56	\N	Nature	How long can a scorpion hold its breath?
57	\N	Nature	What percentage of a cat's bones are located in its tail?
58	\N	Nature	How many brains does an octopus have?
59	\N	Nature	What color is hippopotamus milk?
60	\N	Nature	What animal has the largest eyes in the world?
\.


--
-- Data for Name: triviasession; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.triviasession (t_sessionid, t_starttime, t_stoptime) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (u_userid, u_totalscore, u_username) FROM stdin;
\.


--
-- Name: answers answers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.answers
    ADD CONSTRAINT answers_pkey PRIMARY KEY (a_answerid, a_questionid);


--
-- Name: asked asked_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asked
    ADD CONSTRAINT asked_pkey PRIMARY KEY (as_sessionid, as_questionid, as_answeredby);


--
-- Name: plays plays_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plays
    ADD CONSTRAINT plays_pkey PRIMARY KEY (p_userid, p_sessionid);


--
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (q_questionid);


--
-- Name: triviasession triviasession_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.triviasession
    ADD CONSTRAINT triviasession_pkey PRIMARY KEY (t_sessionid);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (u_userid);


--
-- Name: answers answers_a_questionid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.answers
    ADD CONSTRAINT answers_a_questionid_fkey FOREIGN KEY (a_questionid) REFERENCES public.questions(q_questionid) ON DELETE CASCADE;


--
-- Name: asked asked_as_answeredby_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asked
    ADD CONSTRAINT asked_as_answeredby_fkey FOREIGN KEY (as_answeredby) REFERENCES public.users(u_userid);


--
-- Name: asked asked_as_questionid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asked
    ADD CONSTRAINT asked_as_questionid_fkey FOREIGN KEY (as_questionid) REFERENCES public.questions(q_questionid);


--
-- Name: asked asked_as_sessionid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asked
    ADD CONSTRAINT asked_as_sessionid_fkey FOREIGN KEY (as_sessionid) REFERENCES public.triviasession(t_sessionid);


--
-- Name: plays plays_p_sessionid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plays
    ADD CONSTRAINT plays_p_sessionid_fkey FOREIGN KEY (p_sessionid) REFERENCES public.triviasession(t_sessionid) ON DELETE CASCADE;


--
-- Name: plays plays_p_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plays
    ADD CONSTRAINT plays_p_userid_fkey FOREIGN KEY (p_userid) REFERENCES public.users(u_userid) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

