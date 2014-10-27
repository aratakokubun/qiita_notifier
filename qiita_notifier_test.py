# -*- coding:utf-8 -*-

from qiita_notifier import qiita_notifier

if __name__ == "__main__":
    qin = qiita_notifier()
    qin.check_qiita_action()
    qin.post_weekly_statics()
    qin.post_monthly_statics()
    qin.post_yearly_statics()
