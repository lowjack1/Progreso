import os
from datetime import datetime, timedelta
from dateutil import tz

import aiohttp
from tornado.web import HTTPError, escape
from tornado.ioloop import IOLoop

from .base import BaseHandler


class HomePage(BaseHandler):
    async def get(self):
        action = self.get_argument('action', None)
        if action is None:
            return self.render("homepage.html")

        if action == 'progress_data':
            response_ds = {
                'dp': {
                    'overall': 0,
                    'this_month': 0,
                    'today': 0,
                },
                'graphs': {
                    'overall': 0,
                    'this_month': 0,
                    'today': 0,
                },
                'others': {
                    'overall': 0,
                    'this_month': 0,
                    'today': 0,
                }
            }
            async with self.settings['pool'].acquire() as connection:
                # Get overall data
                q = "SELECT SUM(dp) AS total_dp, SUM(graphs) AS total_graphs, SUM(others) AS total_others FROM track_work;"
                res = await connection.fetchrow(q)

                response_ds['dp']['overall'] = (res['total_dp'] or 0)
                response_ds['graphs']['overall'] = (res['total_graphs'] or 0)
                response_ds['others']['overall'] = (res['total_others'] or 0)

                # Get current month data
                q = '''
                    SELECT SUM(dp) AS total_dp, SUM(graphs) AS total_graphs, SUM(others) AS total_others
                    FROM track_work
                    WHERE date_created >= DATE_TRUNC('month', CURRENT_DATE);
                    '''
                res = await connection.fetchrow(q)

                response_ds['dp']['this_month'] = (res['total_dp'] or 0)
                response_ds['graphs']['this_month'] = (res['total_graphs'] or 0)
                response_ds['others']['this_month'] = (res['total_others'] or 0)

                # Get today's data
                q = '''
                    SELECT SUM(dp) AS total_dp, SUM(graphs) AS total_graphs, SUM(others) AS total_others
                    FROM track_work
                    WHERE date_created >= DATE_TRUNC('day', CURRENT_DATE);
                    '''
                res = await connection.fetchrow(q)

                response_ds['dp']['today'] = (res['total_dp'] or 0)
                response_ds['graphs']['today'] = (res['total_graphs'] or 0)
                response_ds['others']['today'] = (res['total_others'] or 0)
            
            self.write_api_response(response_ds)

        if action == 'programming_line_chart':
            date_unit = self.get_argument('date_unit')
            async with self.settings['pool'].acquire() as connection:
                q = '''
                    SELECT SUM(dp) AS total_dp, SUM(graphs) AS total_graphs, SUM(others) AS total_others, DATE_TRUNC('%s', date_created at time zone '-05:30')::TEXT AS truncated_date
                    FROM track_work
                    GROUP BY truncated_date
                    ORDER BY truncated_date;
                    ''' % date_unit
                res = await connection.fetch(q)

            response_ds = [(_['truncated_date'], _['total_dp'], _['total_graphs'], _['total_others']) for _ in res]
            self.write_api_response(response_ds)


class CreateProgress(BaseHandler):
    async def get(self):
        action = self.get_argument('action', None)
        if action is None:
            return self.render("create_progress.html")
        
        if action == 'todays_record':
            datetime_start = datetime.now(tz.gettz('Asia/Kolkata')).replace(hour=0, minute=0, second=0, microsecond=0)
            async with self.settings['pool'].acquire() as connection:
                q = "SELECT dp::INTEGER, graphs::INTEGER, others::INTEGER, os, sys_des, ml FROM track_work WHERE date_created=$1;"
                res = await connection.fetchrow(q, datetime_start)

            result_ds = []
            if res is not None:
                result_ds = [res['dp'], res['graphs'], res['os'], res['sys_des'], res['ml'], res['others']]

            self.write_api_response(result_ds)

    async def post(self):
        action = self.get_argument('action', None)
        if action == 'create_todays_progress':
            tag = self.get_argument('tag')
            datetime_start = datetime.now(tz.gettz('Asia/Kolkata')).replace(hour=0, minute=0, second=0, microsecond=0)
            async with self.settings['pool'].acquire() as connection:
                q = "SELECT ID FROM track_work WHERE date_created=$1;"
                track_id = await connection.fetchval(q, datetime_start)

                if track_id is None:
                    async with connection.transaction():
                        q = "INSERT INTO track_work (date_created) VALUES($1) RETURNING ID;"
                        track_id = await connection.fetchval(q, datetime_start)

            async with self.settings['pool'].acquire() as connection:
                async with connection.transaction():
                    if tag == 'os':
                        q = "UPDATE track_work SET os=TRUE WHERE ID=$1;"
                        await connection.execute(q, track_id)
                    elif tag == 'sys_des':
                        q = "UPDATE track_work SET sys_des=TRUE WHERE ID=$1;"
                        await connection.execute(q, track_id)
                    elif tag == 'ml':
                        q = "UPDATE track_work SET ml=TRUE WHERE ID=$1;"
                        await connection.execute(q, track_id)
                    elif tag == 'dp':
                        total_problem_solved = int(self.get_body_argument('dp'))
                        q = "UPDATE track_work SET dp=$1 WHERE ID=$2;"
                        await connection.execute(q, total_problem_solved, track_id)
                    elif tag == 'graphs':
                        total_problem_solved = int(self.get_body_argument('graphs'))
                        q = "UPDATE track_work SET graphs=$1 WHERE ID=$2;"
                        await connection.execute(q, total_problem_solved, track_id)
                    elif tag == 'others':
                        total_problem_solved = int(self.get_body_argument('others'))
                        q = "UPDATE track_work SET others=$1 WHERE ID=$2;"
                        await connection.execute(q, total_problem_solved, track_id)

            self.write_api_response(1)