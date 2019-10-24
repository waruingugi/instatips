"""
This data is used in testing main functionalities in tasks not in models!!!

Data for tests comes in pairs to mock previous/non-empty models
and new update/create data in models:
1. existing data
2. new data
"""

# Countries data.
existing_countries_data = [
    {'country': 'Sudan', 'code': 'SD', 'flag': 'https://media.api-football.com/flags/sd.svg'},
    {'country': 'Sweden', 'code': 'SE', 'flag': 'https://media.api-football.com/flags/se.svg'},
    {'country': 'Switzerland', 'code': 'CH', 'flag': 'https://media.api-football.com/flags/ch.svg'},
    {'country': 'Thailand', 'code': 'TH', 'flag': 'https://media.api-football.com/flags/th.svg'},
    {'country': 'Tunisia', 'code': 'TN', 'flag': 'https://media.api-football.com/flags/tn.svg'},
    {'country': 'Turkey', 'code': 'TR', 'flag': 'https://media.api-football.com/flags/tr.svg'},
    {'country': 'Ukraine', 'code': 'UA', 'flag': 'https://media.api-football.com/flags/ua.svg'},
    {'country': 'United-Arab-Emirates', 'code': 'AE', 'flag': 'https://media.api-football.com/flags/ae.svg'},
    {'country': 'Uruguay', 'code': 'UY', 'flag': 'https://media.api-football.com/flags/uy.svg'},
    {'country': 'USA', 'code': 'US', 'flag': 'https://media.api-football.com/flags/us.svg'},
    {'country': 'Uzbekistan', 'code': 'UZ', 'flag': 'https://media.api-football.com/flags/uz.svg'},
    {'country': 'Venezuela', 'code': 'VE', 'flag': 'https://media.api-football.com/flags/ve.svg'},
    {'country': 'Vietnam', 'code': 'VN', 'flag': 'https://media.api-football.com/flags/vn.svg'},
    {'country': 'Wales', 'code': 'GB', 'flag': 'https://media.api-football.com/flags/gb.svg'},
    {'country': 'World', 'code': None, 'flag': None},
    {'country': 'Zambia', 'code': 'ZM', 'flag': 'https://media.api-football.com/flags/zm.svg'},
    {'country': 'Zimbabwe', 'code': 'ZW', 'flag': 'https://media.api-football.com/flags/zw.svg'}
]

new_countries_data = [
    {'country': 'Portugal', 'code': 'PT', 'flag': 'https://media.api-football.com/flags/pt.svg'},
    {'country': 'Qatar', 'code': 'QA', 'flag': 'https://media.api-football.com/flags/qa.svg'},
    {'country': 'Romania', 'code': 'RO', 'flag': 'https://media.api-football.com/flags/ro.svg'},
    {'country': 'Russia', 'code': 'RU', 'flag': 'https://media.api-football.com/flags/ru.svg'},
    {'country': 'Rwanda', 'code': 'RW', 'flag': 'https://media.api-football.com/flags/rw.svg'},
    {'country': 'San-Marino', 'code': 'SM', 'flag': 'https://media.api-football.com/flags/sm.svg'},
    {'country': 'Saudi-Arabia', 'code': 'SA', 'flag': 'https://media.api-football.com/flags/sa.svg'},
    {'country': 'Scotland', 'code': 'GB', 'flag': 'https://media.api-football.com/flags/gb.svg'},
    {'country': 'Senegal', 'code': 'SN', 'flag': 'https://media.api-football.com/flags/sn.svg'},
    {'country': 'Serbia', 'code': 'RS', 'flag': 'https://media.api-football.com/flags/rs.svg'},
    {'country': 'Singapore', 'code': 'SG', 'flag': 'https://media.api-football.com/flags/sg.svg'},
    {'country': 'Slovakia', 'code': 'SK', 'flag': 'https://media.api-football.com/flags/sk.svg'},
    {'country': 'Slovenia', 'code': 'SI', 'flag': 'https://media.api-football.com/flags/si.svg'},
    {'country': 'South-Africa', 'code': 'ZA', 'flag': 'https://media.api-football.com/flags/za.svg'},
    {'country': 'South-Korea', 'code': 'KR', 'flag': 'https://media.api-football.com/flags/kr.svg'},
    {'country': 'Spain', 'code': 'ES', 'flag': 'https://media.api-football.com/flags/es.svg'},
]

# Leagues data.
existing_leagues_data = [
    {'league_id': 984, 'name': 'Primera Division - Clausura', 'type': 'League', 'country': 'Uruguay', 'country_code': 'UY', 'season': 2019, 'season_start': '2019-07-13', 'season_end': '2019-12-07', 'logo': None, 'flag': 'https://media.api-football.com/flags/uy.svg', 'standings': 1, 'is_current': 1, 'coverage': {'standings': True, 'fixtures': {'events': True, 'lineups': True, 'statistics': False, 'players_statistics': False}, 'players': True, 'topScorers': True, 'predictions': True, 'odds': True}},
    {'league_id': 985, 'name': 'W-League', 'type': 'League', 'country': 'Australia', 'country_code': 'AU', 'season': 2019, 'season_start': '2019-11-14', 'season_end': '2020-03-01', 'logo': 'https://media.api-football.com/leagues/243.png', 'flag': 'https://media.api-football.com/flags/au.svg', 'standings': 0, 'is_current': 1, 'coverage': {'standings': False, 'fixtures': {'events': False, 'lineups': False, 'statistics': False, 'players_statistics': False}, 'players': False, 'topScorers': False, 'predictions': True, 'odds': False}},
    {'league_id': 986, 'name': 'Championnat National', 'type': 'League', 'country': 'Benin', 'country_code': 'BJ', 'season': 2019, 'season_start': '2019-10-06', 'season_end': '2019-10-20', 'logo': None, 'flag': 'https://media.api-football.com/flags/bj.svg', 'standings': 0, 'is_current': 1, 'coverage': {'standings': False, 'fixtures': {'events': False, 'lineups': False, 'statistics': False, 'players_statistics': False}, 'players': False, 'topScorers': False, 'predictions': True, 'odds': False}},
    {'league_id': 987, 'name': 'Elite ONE', 'type': 'League', 'country': 'Cameroon', 'country_code': 'CM', 'season': 2020, 'season_start': '2019-10-17', 'season_end': '2020-04-25', 'logo': None, 'flag': 'https://media.api-football.com/flags/cm.svg', 'standings': 1, 'is_current': 1, 'coverage': {'standings': True, 'fixtures': {'events': False, 'lineups': False, 'statistics': False, 'players_statistics': False}, 'players': False, 'topScorers': False, 'predictions': True, 'odds': False}},
]

new_leagues_data = [
    {'league_id': 979, 'name': 'A-League', 'type': 'League', 'country': 'Australia', 'country_code': 'AU', 'season': 2019, 'season_start': '2019-10-11', 'season_end': '2020-04-26', 'logo': 'https://media.api-football.com/leagues/105.png', 'flag': 'https://media.api-football.com/flags/au.svg', 'standings': 1, 'is_current': 1, 'coverage': {'standings': True, 'fixtures': {'events': True, 'lineups': True, 'statistics': True, 'players_statistics': True}, 'players': True, 'topScorers': True, 'predictions': True, 'odds': True}},
    {'league_id': 980, 'name': 'National Soccer League', 'type': 'League', 'country': 'Rwanda', 'country_code': 'RW', 'season': 2019, 'season_start': '2019-10-04', 'season_end': '2019-12-22', 'logo': None, 'flag': 'https://media.api-football.com/flags/rw.svg', 'standings': 1, 'is_current': 1, 'coverage': {'standings': True, 'fixtures': {'events': True, 'lineups': False, 'statistics': False, 'players_statistics': False}, 'players': False, 'topScorers': False, 'predictions': True, 'odds': False}},
    {'league_id': 981, 'name': 'Football League', 'type': 'League', 'country': 'Greece', 'country_code': 'GR', 'season': 2019, 'season_start': '2019-09-28', 'season_end': '2020-03-28', 'logo': 'https://media.api-football.com/leagues/264.png', 'flag': 'https://media.api-football.com/flags/gr.svg', 'standings': 1, 'is_current': 1, 'coverage': {'standings': True, 'fixtures': {'events': True, 'lineups': False, 'statistics': False, 'players_statistics': False}, 'players': True, 'topScorers': True, 'predictions': True, 'odds': True}},
    {'league_id': 982, 'name': 'Football Championship', 'type': 'League', 'country': 'New-Zealand', 'country_code': 'NZ', 'season': 2019, 'season_start': '2019-11-02', 'season_end': '2020-03-29', 'logo': None, 'flag': 'https://media.api-football.com/flags/nz.svg', 'standings': 1, 'is_current': 1, 'coverage': {'standings': True, 'fixtures': {'events': False, 'lineups': False, 'statistics': False, 'players_statistics': False}, 'players': False, 'topScorers': False, 'predictions': True, 'odds': False}},
    {'league_id': 983, 'name': 'Welsh Cup', 'type': 'Cup', 'country': 'Wales', 'country_code': 'GB', 'season': 2019, 'season_start': '2019-10-18', 'season_end': '2019-11-08', 'logo': 'https://media.api-football.com/leagues/280.JPG', 'flag': 'https://media.api-football.com/flags/gb.svg', 'standings': 0, 'is_current': 1, 'coverage': {'standings': False, 'fixtures': {'events': False, 'lineups': False, 'statistics': False, 'players_statistics': False}, 'players': False, 'topScorers': False, 'predictions': True, 'odds': False}},
]