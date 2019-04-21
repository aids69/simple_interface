from django.shortcuts import render
from .forms import NameForm
from keys import accessToken as token
from subprocess import call
import asyncio
import json
import requests
import sys

from .values import values

sys.path.append('../')
from brute_classifier import index


FIELDS = [
    'id',
    'verified', 'sex', 'bdate', 'city', 'country', 'home_town',
    'has_photo', 'online', 'domain', 'has_mobile',
    'contacts', 'site', 'education', 'universities', 'schools',
    'status', 'last_seen', 'followers_count', 'occupation',
    'nickname', 'relatives', 'relation', 'personal', 'connections',
    'exports', 'activities', 'interests', 'music', 'movies',
    'tv', 'books', 'games', 'about', 'quotes', 'screen_name',
    'timezone', 'maiden_name', 'career', 'military'
]
GROUP_FIELDS = [
    'members_count', 'verified', 'activity',
    'age_limits', 'description', 'status', 'trending'
]
URL = 'https://api.vk.com/method/'
GET_USERS = 'users.get?'
GET_GROUPS = 'groups.get?'
GET_DETAILED_GROUPS = 'groups.getById?'


def basic(request):
    if request.method == 'POST':
        return prediction(request)
    return render(request, 'index.html')


def get_user_data(id):
    res = requests.get('{}{}user_ids={}&v=5.21&access_token={}&fields={}'
                       .format(URL, GET_USERS, id, token, ','.join(FIELDS)))
    return json.loads(res.content.decode())['response'][0]


def get_group_data(id):
    """
        Returns json with communities:
        {'count': 9, 'items': [124350, 342746743, 7435262,...]}
    """
    res = requests.get('{}{}user_id={}&v=5.21&access_token={}&count=1000'
                       .format(URL, GET_GROUPS, id, token))
    return json.loads(res.content.decode())['response']


def get_detailed_groups_info(ids):
    ids = [str(id) for id in ids]
    res = requests.get('{}{}group_ids={}&v=5.21&access_token={}&fields={}'
                       .format(URL, GET_DETAILED_GROUPS, ','.join(ids), token, ','.join(GROUP_FIELDS)))
    return json.loads(res.content.decode())['response']


def prediction(request):
    form = NameForm(request.POST)
    id = form.data['prediction']

    user = get_user_data(id)
    id = user['id']  # for cases where screen_name is passed
    communities_ids = get_group_data(id)['items'][:26]
    communities = get_detailed_groups_info(communities_ids) if communities_ids else []

    results = index.new_proccess_req(id, user, communities)
    vals = [values[result] for result in results]

    results = [str(result) for result in results]

    return render(request, 'prediction.html',
                  {'ids': results,
                   'name': '{} {}'.format(user['first_name'], user['last_name']),
                   'values': vals})
