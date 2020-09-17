from piazza_api import Piazza
from piazza_api import network as net
from discord import Webhook, AsyncWebhookAdapter, Embed
from secrets import p_pass, p_email, p_network, d_url
import sqlite3, html, aiohttp, asyncio

prepped_posts = []
cooked_posts = []

def find_new_posts(limit=50):
    p_instance = Piazza()
    p_instance.user_login(p_email, p_pass)
    ds = p_instance.network(p_network)
    ds_posts = ds.get_filtered_feed(net.UnreadFilter())
    if len(ds_posts['feed']) > 0:
        for x in range(0, len(ds_posts['feed'])):
            tags = ds_posts['feed'][x]['tags']
            if 'instructor-note' not in tags:
                prepped_posts.append(ds_posts['feed'][x])

async def cook_prepped_posts():
    if len(prepped_posts) > 0:
        for prepped_post in prepped_posts:
            # Does the database contain the id?
            if not db_has_id(prepped_post['id']):
                # Db doesn't contain entry, add it then notify the web-hook.
                c.execute('''INSERT INTO read_posts(id) values(?)''', (prepped_post['id'],))
                conn.commit()
                cooked_posts.append(prepped_post)
        # Drop prepped list
        prepped_posts[:] = []
        # Send-off to the web-hook
        for cooked_post in cooked_posts:
            #print(cooked_post)
            post_url = 'https://piazza.com/class/' + str(cooked_post["nid"]) + "?cid=" + str(cooked_post["nr"])
            post_content = html.unescape(cooked_post["content_snipet"])
            title = cooked_post["subject"]
            desc = "<" + post_url + ">\n" + post_content
            
            embed = Embed(title=str(title), description=str(desc), color=000000)
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(d_url, adapter=AsyncWebhookAdapter(session))
                await webhook.send(embed=embed)
    else:
        print('No new unread posts found.')

def db_has_id(post_id):
    c.execute('''SELECT * FROM read_posts WHERE id LIKE ?''', (post_id,))
    return True if c.fetchone() is not None else False

if __name__ == '__main__':
    find_new_posts()
    conn = sqlite3.connect('read_posts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS read_posts (id text)''')  
    loop = asyncio.get_event_loop()
    loop.run_until_complete(cook_prepped_posts())
    loop.close()
    c.close()
