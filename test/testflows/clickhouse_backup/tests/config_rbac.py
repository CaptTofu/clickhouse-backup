import os
import time
from pathlib import Path

from testflows.core import *
from testflows.asserts import *

from clickhouse_backup.requirements.requirements import *
from clickhouse_backup.tests.steps import *


@TestScenario
@Requirements(
    RQ_SRS_013_ClickHouse_BackupUtility_Configs_Backup("1.0"),
    RQ_SRS_013_ClickHouse_BackupUtility_Configs_Restore("1.0")
)
def configs_backup_restore(self):
    """Test that configs can be backed up and restored.
    """
    ch_node = self.context.nodes[0]
    backup = self.context.backup
    table_name = "config_bp"
    files_contents = {}

    try:
        with Given("I create and populate table"):
            create_and_populate_table(node=ch_node, table_name=table_name)

        with And("I make sure some configuration files/directories exist"):
            for dirname in ("configs/clickhouse1/config.d", "configs/clickhouse1/users.d"):
                if not Path(dirname).is_dir():
                    with By(f"creating new dir {dirname}"):
                        os.mkdir(dirname)

            for filename in ("configs/clickhouse1/config.xml", "configs/clickhouse1/users.xml",
                             "configs/clickhouse1/config.d/macros.xml", "configs/clickhouse1/users.d/users_d.xml"):
                if not Path(filename).is_file():
                    with By(f"creating new file {filename}"):
                        with open(filename, "w") as file:
                            file.write("<yandex></yandex>")

        with When(f"I create backup"):
            backup.cmd(f"clickhouse-backup create --configs {table_name}")

        with When("I remove existing configuration to restore it later"):
            for root, dirs, files in os.walk("configs/clickhouse1", topdown=False):
                for file in files:
                    filename = f"{root[20:]}/{file}"
                    files_contents[filename] = ch_node.cmd(f"cat /etc/clickhouse-server/{filename}").output
                    ch_node.cmd(f"echo \"\" > /etc/clickhouse-server/{filename}")

        with Then("I restore from the backup and restart"):
            r = backup.cmd(f"clickhouse-backup restore --configs {table_name}", exitcode=None)

            with Then("I expect ch-backup to attempt restart ch-server"):
                assert "restart clickhouse-server" in r.output, error()

            with And("I restart clickhouse"):
                ch_node.restart(safe=False)

        with And("I check files restored correctly"):
            for root, dirs, files in os.walk("configs/clickhouse1", topdown=False):
                for name in files:
                    filename = f"{root[20:]}/{name}"
                    assert files_contents[filename] == ch_node.cmd(f"cat /etc/clickhouse-server/{filename}").output, error()

    finally:
        with Finally("removing created backup"):
            backup.cmd(f"clickhouse-backup delete local {table_name}")


@TestScenario
@Requirements(
    RQ_SRS_013_ClickHouse_BackupUtility_RBAC_Backup("1.0"),
    RQ_SRS_013_ClickHouse_BackupUtility_RBAC_Restore("1.0")
)
def rbac_backup_restore(self):
    """Test that RBAC objects can be backed up and restored.
    """
    ch_node = self.context.nodes[0]
    backup = self.context.backup
    table_name = "rbac_bp"

    try:
        with Given("I create and populate table"):
            create_and_populate_table(node=ch_node, table_name=table_name)

        with And("I create RBAC objects to be backed up"):
            for o, n in (("USER", "test_user"), ("ROLE", "test_role"), ("ROW POLICY", "test_policy ON rbac_bp"),
                         ("SETTINGS PROFILE", "test_profile"), ("QUOTA", "test_quota")):
                ch_node.query(f"CREATE {o} {n}")

        with When(f"I create backup"):
            backup.cmd(f"clickhouse-backup create --rbac {table_name}")

        with And("I delete objects to be backed up"):
            for o, n in (("USER", "test_user"), ("ROLE", "test_role"), ("ROW POLICY", "test_policy ON rbac_bp"),
                         ("SETTINGS PROFILE", "test_profile"), ("QUOTA", "test_quota")):
                ch_node.query(f"DROP {o} IF EXISTS {n}")
            ch_node.restart()


        with Then("I restore from the backup and restart"):
            backup.cmd(f"clickhouse-backup restore --rbac {table_name}", exitcode=None)
            ch_node.restart()

        with And("I check objects rstored correctly"):
            with By("expect user restored"):
                assert "test_user" in ch_node.query("SHOW USERS").output, error()

            with And("expect role restored"):
                assert "test_role" in ch_node.query("SHOW ROLES").output, error()

            with And("expect row policy restored"):
                assert "test_policy" in ch_node.query("SHOW ROW POLICIES").output, error()

            with And("expect settings profile restored"):
                assert "test_profile" in ch_node.query("SHOW SETTINGS PROFILES").output, error()

            with And("expect quota restored"):
                assert "test_quota" in ch_node.query("SHOW QUOTAS").output, error()

            for o, n in (("USER", "test_user"), ("ROLE", "test_role"), ("ROW POLICY", "test_policy ON rbac_bp"),
                         ("SETTINGS PROFILE", "test_profile"), ("QUOTA", "test_quota")):
                ch_node.query(f"DROP {o} IF EXISTS {n}")

    finally:
        with Finally("removing created backup"):
            backup.cmd(f"clickhouse-backup delete local {table_name}")


@TestFeature
def config_rbac(self):
    """Check that configs and RBAC backups can be created and restored.
    """
    for scenario in loads(current_module(), Scenario, Suite):
        Scenario(run=scenario)