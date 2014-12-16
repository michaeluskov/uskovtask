# -*- coding: utf-8 -*-

from uskovapp.models import Polls, PollVariants, Votes
from django.db.models import Count
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import StringIO


def createPollPic(poll_id):
    poll_text = Polls.objects.filter(pk=poll_id).values('text')[:1][0]['text']
    variants = PollVariants.objects.filter(poll_id=poll_id).annotate(votes_num=Count('votes'))
    max_votes_num = sum([i.votes_num for i in variants]) or 1   
    image = PIL.Image.new('RGB',(440, 30+len(variants)*16), '#ffffff')
    font = PIL.ImageFont.truetype('uskovapp/Helvetica_Light-Normal.ttf', size=18, encoding='utf-8')
    draw = PIL.ImageDraw.Draw(image)
    draw.text((15,3), poll_text, fill='#000000', font=font)
    i = 0
    for variant in variants:
        y = 25 + i * 16
        x = 3
        i += 1
        height = 10
        width = 395 * (float(variant.votes_num)/max_votes_num)
        if variant.votes_num == 0:
            width = 3
        draw.rectangle(((x,y), (x+width,y+height)), fill='#000000')
        draw.text((405, y), str(variant.votes_num), fill='#000000', font=font)
    io = StringIO.StringIO()
    image.save(io, format='PNG')
    return io.getvalue()