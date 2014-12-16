from uskovapp.models import Polls, PollVariants, Votes
from django.db.models import Count
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont


def createPollPic(poll_id):
    poll_text = Polls.objects.filter(pk=poll_id).values('text')[:1][0]['text']
    variants = PollVariants.objects.filter(poll_id=poll_id).annotate(votes_num=Count('votes'))
    