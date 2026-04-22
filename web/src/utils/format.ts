import {PermissionAssign} from "@/api/permissionApi.ts";
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';
import duration from 'dayjs/plugin/duration';

dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.extend(duration);

export const formatAllowAssignText = (assign: PermissionAssign): string => {
    const startTime = dayjs(assign.startTime).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss');
    const endTime = assign.endTime
        ? dayjs(assign.endTime).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
        : '永久';
    return `将【${assign.grantObjectName}】授权给【${assign.granteeObjectName}】，从 ${startTime} 至 ${endTime}`;
};

export const formatDenyAssignText = (assign: PermissionAssign): string => {
    const startTime = dayjs(assign.startTime).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss');
    const endTime = assign.endTime
        ? dayjs(assign.endTime).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
        : '永久';
    return `拒绝【${assign.granteeObjectName}】使用【${assign.grantObjectName}】，从 ${startTime} 至 ${endTime}`;
};


export const formatAllowAssignShortText = (assign: PermissionAssign): string => {
    const startTime = dayjs(assign.startTime).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss');
    const endTime = assign.endTime
        ? dayjs(assign.endTime).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
        : '永久';
    return `授权给【${assign.granteeObjectName}】，从 ${startTime} 至 ${endTime}`;
};

export const formatDenyAssignShortText = (assign: PermissionAssign): string => {
    const startTime = dayjs(assign.startTime).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss');
    const endTime = assign.endTime
        ? dayjs(assign.endTime).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
        : '永久';
    return `拒绝【${assign.granteeObjectName}】使用，从 ${startTime} 至 ${endTime}`;
};