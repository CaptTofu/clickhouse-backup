package backup

import (
	"context"
	"github.com/Altinity/clickhouse-backup/v2/pkg/status"
)

func (b *Backuper) CreateToRemote(backupName string, deleteSource bool, diffFrom, diffFromRemote, tablePattern string, partitions, skipProjections []string, schemaOnly, backupRBAC, rbacOnly, backupConfigs, configsOnly, skipCheckPartsColumns, resume bool, version string, commandId int) error {
	ctx, cancel, err := status.Current.GetContextWithCancel(commandId)
	if err != nil {
		return err
	}
	ctx, cancel = context.WithCancel(ctx)
	defer cancel()
	if backupName == "" {
		backupName = NewBackupName()
	}
	if err := b.CreateBackup(backupName, diffFromRemote, tablePattern, partitions, schemaOnly, backupRBAC, rbacOnly, backupConfigs, configsOnly, skipCheckPartsColumns, skipProjections, resume, version, commandId); err != nil {
		return err
	}
	if err := b.Upload(backupName, deleteSource, diffFrom, diffFromRemote, tablePattern, partitions, skipProjections, schemaOnly, rbacOnly, configsOnly, resume, version, commandId); err != nil {
		return err
	}

	return nil
}
