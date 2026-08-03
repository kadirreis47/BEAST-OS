def register_commands(sub):
 d=sub.add_parser('dashboard');d.set_defaults(handler=lambda a:print('Dashboard ready'))
 t=sub.add_parser('today');t.set_defaults(handler=lambda a:print("Today's planner"))
 s=sub.add_parser('stats');s.set_defaults(handler=lambda a:print('Analytics'))
