
from beastos.storage.sqlite.dashboard_repository import DashboardRepository,DashboardSnapshot

def test_repository_roundtrip(tmp_path):
    repo=DashboardRepository(str(tmp_path/'db.sqlite'))
    snap=DashboardSnapshot(82.5,3,6,81.0,240)
    repo.save(snap)
    loaded=repo.latest()
    assert loaded==snap
