from stages.ControlUnit import BaseStage, ControlUnit
from Instructions import Instruction, Format


class MEMStage(BaseStage):
    def __init__(self, ParentUnit: ControlUnit):
        super().__init__(ParentUnit)

    def execute(
        self,
        pc: int,
        instruction: Instruction,
        control: dict,
        ReadData2: int,
        ALUresult: int,
        AddrResult: int,
        RegDstValue: str,  # 這個是要存到哪個暫存器 在EXStage已經算好了 傳下去
    ):
        super().execute()
        if control["MemWrite"] == 1:  # 大概是sw會用到
            self._ControlUnit._MemAndReg.setMem(ALUresult, ReadData2)
            self.output = {
                "PC": pc,
                "instruction": instruction,
                "nop": self.nop,
                "ALUResult": ALUresult,
                "ReadData": None,
                "RegDstValue": RegDstValue,
            }
        if control["MemRead"] == 1:
            # 從mem array 讀出 ReadData就是如果lw有讀出來的話 要送到wb的值
            ReadData = self._ControlUnit._MemAndReg.getMem(ALUresult)
            self.output = {
                "PC": pc,
                "instruction": instruction,
                "nop": self.nop,
                "ALUResult": ALUresult,
                "ReadData": ReadData,
                "RegDstValue": RegDstValue,
            }
        elif control["Branch"] == 1:
            if ALUresult==0:
                self.output = {
                    "PC": AddrResult,
                    "instruction": instruction,
                    "nop": self.nop,
                    "ALUResult": ALUresult,
                    "ReadData": None,
                    "RegDstValue": RegDstValue,
                }
            else:
                self.output = {
                    "PC": pc,
                    "instruction": instruction,
                    "nop": self.nop,
                    "ALUResult": ALUresult,
                    "ReadData": None,
                    "RegDstValue": RegDstValue,
                }
        else:
            self.output = {
                "PC": pc,
                "instruction": instruction,
                "nop": self.nop,
                "ALUResult": ALUresult,
                "ReadData": None,
                "RegDstValue": RegDstValue,
            }
        # if control["branch"] == 1:
        # undo

        # 該stage 要傳給下一個stage的 control 值
        self.output["control"] = {}
        for c in ["MemToReg", "RegWrite"]:
            self.output["control"][c] = control[c]
        return self.output
