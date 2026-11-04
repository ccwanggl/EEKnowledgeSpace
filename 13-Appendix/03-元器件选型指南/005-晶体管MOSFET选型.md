---
tags: [appendix, components, selection, guide]
date-created: 2026-06-15
---

# 晶体管/MOSFET 选型

## BJT（双极型晶体管）
- **$h_{FE}$（β）**：电流增益，几十到几百
- **$V_{CE(sat)}$**：饱和压降，越低越好
- **$I_{C(max)}$、$P_{D(max)}$**：最大电流和功耗
- **$f_T$**：特征频率，高频应用注意
- **封装**：SOT-23、SOT-89、TO-92、TO-220
- **常用**：2N2222（NPN）、2N2907（PNP）、BC547、S8050

### MOSFET
- **$V_{GS(th)}$**：阈值电压，逻辑电平 MOSFET < 2V
- **$R_{DS(on)}$**：导通电阻，越低损耗越小，与耐压 trade-off
- **$V_{DS(max)}$**：最大漏源电压
- **$Q_g$**：栅极总电荷，影响驱动损耗和开关速度
- **封装**：SOT-23、SO-8、DPAK、D2PAK、TO-220、TO-247
- **逻辑电平**：AO3400、SI2302、IRLML2502（3.3V 可驱动）
- **功率**：IRFZ44N、IRF3205、AOD514、TPN2R304PL
- **PMOS**：IRF9540、AO3401（高侧开关）

### 选型要点
- 低电压小电流（<1A）：SOT-23 逻辑电平 MOSFET
- 中功率（1~10A）：SO-8 或 DPAK，注意热设计
- 高功率（>10A）：D2PAK/TO-220，必须加散热
- 高速开关：关注 $Q_g$ 和 $C_{iss}$，驱动电路设计

---

