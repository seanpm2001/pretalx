from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from i18nfield.fields import I18nCharField, I18nTextField

from pretalx.common.mixins import LogMixin
from pretalx.common.urls import EventUrls


class CfP(LogMixin, models.Model):
    event = models.OneToOneField(
        to='event.Event',
        on_delete=models.PROTECT,
    )
    headline = I18nCharField(
        max_length=300,
        null=True, blank=True,
        verbose_name=_('headline'),
    )
    text = I18nTextField(
        null=True, blank=True,
        verbose_name=_('text'),
        help_text=_('You can use markdown here.'),
    )
    default_type = models.ForeignKey(
        to='submission.SubmissionType',
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name=_('Default submission type'),
    )
    deadline = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('deadline'),
        help_text=_('Please put in the last date you want to accept submissions from users.'),
    )

    class urls(EventUrls):
        base = '{self.event.orga_urls.cfp}'
        questions = '{base}/questions'
        new_question = '{questions}/new'
        text = '{base}/text'
        edit_text = '{text}/edit'
        types = '{base}/types'
        new_type = '{types}/new'
        public = '{self.event.urls.base}/cfp'

    def __str__(self) -> str:
        return f'CfP(event={self.event.slug})'

    @property
    def is_open(self):
        _now = now()
        if self.deadline is None:
            return True
        if self.deadline >= _now:
            return True
        return any(t.deadline >= _now for t in self.event.submission_types.filter(deadline__isnull=False))
