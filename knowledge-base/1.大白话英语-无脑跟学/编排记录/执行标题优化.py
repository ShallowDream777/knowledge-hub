"""保存修改前快照，应用标题及链接迁移；不重建任何课程。"""
from pathlib import Path
import hashlib
import json
import re
from 标题优化 import VAULT, reader_files, rename_text

RECORD=Path(__file__).resolve().parent
BACKUP=RECORD/'标题优化前快照'

def sha(data):
    return hashlib.sha256(data).hexdigest()

if __name__=='__main__':
    report_path=RECORD/'标题调整明细.json'
    assert not report_path.exists(),'迁移已经执行；后续使用标题优化模块逐文件更新，避免覆盖首次审计记录。'
    files=reader_files()
    report={'检查文件数':len(files),'修改文件':[],'范围':'原标题、目录文字和链接锚点；不改知识段落、例句、题答、文件名及学习进度。'}
    for path in files:
        before=path.read_bytes()
        text=before.decode('utf-8')
        after_text=rename_text(text,path)
        after=after_text.encode('utf-8')
        if before==after:
            continue
        relative=path.relative_to(VAULT)
        snapshot=BACKUP/(str(relative)+'.snapshot')
        snapshot.parent.mkdir(parents=True,exist_ok=True)
        snapshot.write_bytes(before)
        oldheads=re.findall(r'^#{1,6} ([^\r\n]+)',text,re.M)
        newheads=re.findall(r'^#{1,6} ([^\r\n]+)',after_text,re.M)
        assert len(oldheads)==len(newheads)
        report['修改文件'].append({'文件':relative.as_posix(),'修改前SHA256':sha(before),'修改后SHA256':sha(after),
                                 '标题':[{'原标题':a,'新标题':b} for a,b in zip(oldheads,newheads) if a!=b]})
        path.write_bytes(after)
    report['修改标题数']=sum(len(row['标题']) for row in report['修改文件'])
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

    # 来源资料仅作标题改名：更新当前来源哈希，旧字节与旧哈希保留在上面的审计记录。
    mapping_path=RECORD/'来源映射.json'
    mapping=json.loads(mapping_path.read_text(encoding='utf-8'))
    mapping['原文件SHA256']={name:sha((VAULT/name).read_bytes()) for name in mapping['原文件SHA256']}
    mapping_path.write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'检查文件':len(files),'修改文件':len(report['修改文件']),'修改标题':report['修改标题数']},ensure_ascii=False))
