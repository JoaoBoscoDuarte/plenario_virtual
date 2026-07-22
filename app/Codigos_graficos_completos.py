import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.family']='DejaVu Sans'
AZUL='#2563EB'; AZUL_CLARO='#93C5FD'; CINZA='#9CA3AF'; VERDE='#059669'
ESC='#111827'; MED='#4B5563'; VERM='#C00000'; ROXO='#7C3AED'
def base(fs=(8,4.6),bottom_axis=True):
    fig,ax=plt.subplots(figsize=fs,dpi=300)
    for s in ax.spines.values(): s.set_visible(False)
    if bottom_axis:
        ax.spines['bottom'].set_visible(True); ax.spines['bottom'].set_color('#D1D5DB')
    ax.tick_params(length=0)
    return fig,ax
def titulo(fig,h,sub=None,y=0.955,ys=0.90,fs=13,fss=10):
    fig.text(0.02,y,h,fontsize=fs,fontweight='bold',color=ESC,ha='left',va='top')
    if sub: fig.text(0.02,ys,sub,fontsize=fss,color=MED,ha='left',va='top')
def fonte(fig,extra=''):
    t='Fonte: elaboração própria a partir de dados do portal de transparência do STF.'
    fig.text(0.02,0.015,(extra+' ' if extra else '')+t,fontsize=7.5,color='#6B7280',ha='left')
def br(v,d=0):
    if d==0: return f'{int(round(v)):,}'.replace(',','.')
    return f'{v:.{d}f}'.replace('.',',')
import pandas as pd, numpy as np
from estilo import *
ac = pd.read_csv('/mnt/user-data/uploads/acervo_baixa_distribuicao.csv').sort_values('Ano').reset_index(drop=True)
anos = ac['Ano'].astype(int).tolist()
ADI=ac['ADI Ativos'].astype(int).tolist(); ADPF=ac['ADPF Ativos'].astype(int).tolist()
ADC=ac['ADC Ativos'].astype(int).tolist(); ADO=ac['ADO Ativos'].astype(int).tolist()
PRETO='#000000'
def idx(a): return anos.index(a)
# posição proporcional ao mês: centro da coluna do ano = idx; deslocamento = (mês-6.5)/12
def pos_mes(ano,mes,dia=15):
    frac=((mes-1)+ (dia-1)/30)/12   # 0..1 dentro do ano
    return idx(ano) - 0.5 + frac    # borda esquerda da coluna + fração
ER=[(pos_mes(2016,6,22),'ER','51'),(pos_mes(2019,6,14),'ER','52'),(pos_mes(2020,3,18),'ER','53')]
ESP0=pos_mes(2020,2,3); ESP1=pos_mes(2022,4,22)

fig,ax=plt.subplots(figsize=(12,5.4),dpi=300)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0,colors=PRETO)
x=np.arange(len(anos))
ax.bar(x,ADI,color=AZUL,zorder=3,label='ADI')
ax.bar(x,ADPF,bottom=ADI,color=VERDE,zorder=3,label='ADPF')
ax.bar(x,ADC,bottom=[ADI[i]+ADPF[i] for i in range(len(anos))],color=ROXO,zorder=3,label='ADC')
ax.bar(x,ADO,bottom=[ADI[i]+ADPF[i]+ADC[i] for i in range(len(anos))],color=CINZA,zorder=3,label='ADO')
ax.set_xticks(x); ax.set_xticklabels(anos,fontsize=9.5,color=PRETO,rotation=90,fontweight='bold')
ax.set_yticks([]); ax.set_ylim(0,2600)

for pos,er,num in ER:
    ax.axvline(pos,color=PRETO,lw=1.0,ls=(0,(4,3)),zorder=5,ymax=0.93)
    ax.text(pos,2510,er,fontsize=8.5,color=PRETO,ha='center',va='bottom',fontweight='bold',zorder=6)
    ax.text(pos,2420,num,fontsize=8.5,color=PRETO,ha='center',va='bottom',fontweight='bold',zorder=6)

ax.axvspan(ESP0,ESP1,color="#FCE7F3",alpha=0.55,zorder=0)
ax.axvline(ESP0,color=VERM,lw=1.0,ls=(0,(4,3)),zorder=5,ymax=0.93)
ax.axvline(ESP1,color=VERM,lw=1.0,ls=(0,(4,3)),zorder=5,ymax=0.93)
ax.annotate('',xy=(ESP1,1950),xytext=(ESP0,1950),arrowprops=dict(arrowstyle='<->',color=VERM,lw=1.0),zorder=6)
ax.text((ESP0+ESP1)/2,1990,'ESPIN',fontsize=8.5,color=VERM,ha='center',va='bottom',fontweight='bold',zorder=6)

ax.legend(frameon=False,fontsize=10,ncol=4,loc='upper left',labelcolor=PRETO)
fig.text(0.02,0.965,'O acervo de controle concentrado, por classe, 1988-2025',
         fontsize=13.5,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.915,'Processos ativos em 31 de dezembro de cada ano',fontsize=10.5,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.86,bottom=0.10,left=0.03,right=0.99)
plt.savefig('../FINAL/1b_acervo_por_classe_1988-2025.png',facecolor='white'); plt.close()
print('ER51 x=%.2f | ER52 x=%.2f | ER53 x=%.2f | ESPIN %.2f a %.2f'%(ER[0][0],ER[1][0],ER[2][0],ESP0,ESP1))
import pandas as pd, numpy as np
from estilo import *
PRETO='#000000'
ac = pd.read_csv('/mnt/user-data/uploads/acervo_baixa_distribuicao.csv').sort_values('Ano').reset_index(drop=True)
anos = ac['Ano'].astype(int).tolist()
ADI=ac['ADI Ativos'].astype(int).tolist(); ADPF=ac['ADPF Ativos'].astype(int).tolist()
ADC=ac['ADC Ativos'].astype(int).tolist(); ADO=ac['ADO Ativos'].astype(int).tolist()
def idx(a): return anos.index(a)
def pos_mes(ano,mes,dia=15): return idx(ano)-0.5+((mes-1)+(dia-1)/30)/12
ER=[(pos_mes(2016,6,22),'ER 51'),(pos_mes(2019,6,14),'ER 52'),(pos_mes(2020,3,18),'ER 53')]
ESP0=pos_mes(2020,2,3); ESP1=pos_mes(2022,4,22)

fig,ax=plt.subplots(figsize=(7.4,10.4),dpi=300)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0,colors=PRETO)
y=np.arange(len(anos))
ax.barh(y,ADI,color=AZUL,zorder=3,label='ADI')
ax.barh(y,ADPF,left=ADI,color=VERDE,zorder=3,label='ADPF')
ax.barh(y,ADC,left=[ADI[i]+ADPF[i] for i in range(len(anos))],color=ROXO,zorder=3,label='ADC')
ax.barh(y,ADO,left=[ADI[i]+ADPF[i]+ADC[i] for i in range(len(anos))],color=CINZA,zorder=3,label='ADO')
tot=[ADI[i]+ADPF[i]+ADC[i]+ADO[i] for i in range(len(anos))]
for i,t in enumerate(tot):
    ax.text(t+28,i,br(t),va='center',ha='left',fontsize=12,color=PRETO,fontweight='bold',zorder=6)
ax.set_yticks(y); ax.set_yticklabels(anos,fontsize=9.5,color=PRETO,fontweight='bold')
ax.invert_yaxis()
ax.set_xlim(0,2680); ax.set_xticks([])
# ER: linha horizontal tracejada preta na fração do mês; rótulo à direita, ACIMA da linha, sem tocar, negrito
for pos,lab in ER:
    ax.axhline(pos,color=PRETO,lw=1.0,ls=(0,(4,3)),zorder=5,xmax=0.90)
    ax.text(2650,pos,lab,fontsize=10,color=PRETO,va='center',ha='right',fontweight='bold',zorder=6)
# ESPIN: sombreado + 2 linhas vermelhas nas frações exatas + seta vertical + rótulo sem data
ax.axhspan(ESP0,ESP1,color="#FCE7F3",alpha=0.55,zorder=0)
ax.axhline(ESP0,color=VERM,lw=1.0,ls=(0,(4,3)),zorder=5,xmax=0.90)
ax.axhline(ESP1,color=VERM,lw=1.0,ls=(0,(4,3)),zorder=5,xmax=0.90)
ax.annotate('',xy=(2380,ESP1),xytext=(2380,ESP0),arrowprops=dict(arrowstyle='<->',color=VERM,lw=1.1),zorder=6)
ax.text(2145,(ESP0+ESP1)/2,'ESPIN',fontsize=10,color=VERM,va='center',ha='left',fontweight='bold',zorder=6)
ax.legend(frameon=False,fontsize=10,ncol=1,loc='upper right',labelcolor=PRETO,bbox_to_anchor=(0.995,0.995))
fig.text(0.02,0.972,'O acervo de controle concentrado, por classe, 1988-2025',
         fontsize=13.5,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.952,'Processos ativos em 31 de dezembro de cada ano',fontsize=10.5,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.94,bottom=0.02,left=0.085,right=0.985)
plt.savefig('../FINAL/1b2_acervo_por_classe_horizontal_1988-2025.png',facecolor='white'); plt.close()
print('1.b2 gerado')
import pandas as pd, numpy as np
from estilo import *
PRETO='#000000'
ac = pd.read_csv('/mnt/user-data/uploads/acervo_baixa_distribuicao.csv').sort_values('Ano').reset_index(drop=True)
anos = ac['Ano'].astype(int).tolist()
dist = ac['Total Distribuídos'].astype(int).tolist()
baix = ac['Total Baixas'].astype(int).tolist()
var  = [d-b for d,b in zip(dist,baix)]
def idx(a): return anos.index(a)
def pos_mes(ano,mes,dia=15): return idx(ano)-0.5+((mes-1)+(dia-1)/30)/12
ER=[(pos_mes(2016,6,22),'51'),(idx(2019)-0.5,'52'),(idx(2020)-0.5,'53')]
ESP0=pos_mes(2020,2,3); ESP1=pos_mes(2022,4,22)
x=np.arange(len(anos))

# ============ 1.c (layout salvo + números 572, 797, 251; pontilhados mais altos) ============
YMIN=-int(max(baix)*1.15)
YMAX=int(max(dist)*1.30)
fig,ax=base((12,7.2))
ax.bar(x,dist,0.8,color=AZUL,zorder=3,label='Distribuição')
ax.bar(x,[-b for b in baix],0.8,color=CINZA,zorder=3,label='Baixa')
ax.axhline(0,color=PRETO,lw=1)
ax.set_xticks(x); ax.set_xticklabels(anos,fontsize=9.5,color=PRETO,rotation=90,fontweight='bold')
ax.set_yticks([]); ax.set_ylim(YMIN,YMAX); ax.tick_params(colors=PRETO)
LT=0.95
er_ys=[YMAX*0.92,YMAX*0.80,YMAX*0.68]
for (pos,num),yl in zip(ER,er_ys):
    ax.axvline(pos,color=PRETO,lw=1.0,ls=(0,(4,3)),zorder=5,ymax=LT)
    ax.text(pos,yl+20,'ER',fontsize=10,color=PRETO,ha='center',va='bottom',fontweight='bold',zorder=6)
    ax.text(pos,yl-30,num,fontsize=10,color=PRETO,ha='center',va='bottom',fontweight='bold',zorder=6)
ESP0=idx(2020)-0.5; ESP1=idx(2022)+0.5
esp_y=YMAX*0.86
ax.axvspan(ESP0,ESP1,color=VERDE,alpha=0.35,zorder=0)
ax.axvline(ESP1,color=VERM,lw=1.0,ls=(0,(4,3)),zorder=5,ymax=LT)
ax.text((ESP0+ESP1)/2,esp_y,'ESPIN',fontsize=10,color=VERM,ha='center',va='bottom',fontweight='bold',zorder=6)
# números citados no texto: 572 (2021, distto), 797 (2020, baixa), 251 (2025, dist)
ax.text(idx(2021),dist[idx(2021)]+18,'572',ha='center',va='bottom',fontsize=11.5,fontweight='bold',color=PRETO,zorder=6)
ax.text(idx(2020),-baix[idx(2020)]-20,'797',ha='center',va='top',fontsize=11.5,fontweight='bold',color=PRETO,zorder=6)
ax.text(idx(2025),dist[idx(2025)]+18,'251',ha='center',va='bottom',fontsize=11.5,fontweight='bold',color=PRETO,zorder=6)
ax.text(idx(2023),dist[idx(2023)]+18,'336',ha='center',va='bottom',fontsize=11.5,fontweight='bold',color=PRETO,zorder=6)
ax.text(idx(2023),-baix[idx(2023)]-20,'608',ha='center',va='top',fontsize=11.5,fontweight='bold',color=PRETO,zorder=6)
ax.legend(frameon=False,fontsize=10.5,loc='lower left',labelcolor=PRETO)
fig.text(0.02,0.965,'A baixa supera a distribuição a partir de 2018',
         fontsize=13.5,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.915,'Distribuição (acima) e baixa (abaixo) de processos de controle concentrado, por ano, 1988-2025',
         fontsize=10.5,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.86,bottom=0.10,left=0.03,right=0.99)
plt.savefig('../FINAL/1c_distribuicao_baixa_espelhado_1988-2025.png',facecolor='white'); plt.close()

# ============ 1.d (layout salvo + números -112 e -137; pontilhados mais altos) ============
YMIN,YMAX=-380,520
fig,ax=base((12,5.6))
cores=[CINZA if v>=0 else VERM for v in var]
ax.bar(x,var,0.8,color=cores,zorder=3)
ax.axhline(0,color=PRETO,lw=1)
ax.set_xticks(x); ax.set_xticklabels(anos,fontsize=9.5,color=PRETO,rotation=90,fontweight='bold')
ax.set_yticks([]); ax.set_ylim(YMIN,YMAX); ax.tick_params(colors=PRETO)
LT=(390-YMIN)/(YMAX-YMIN)
for pos,num in ER:
    ax.axvline(pos,color=PRETO,lw=1.0,ls=(0,(4,3)),zorder=5,ymax=LT)
    ax.text(pos,462,'ER',fontsize=10,color=PRETO,ha='center',va='bottom',fontweight='bold',zorder=6)
    ax.text(pos,410,num,fontsize=10,color=PRETO,ha='center',va='bottom',fontweight='bold',zorder=6)
ax.axvspan(ESP0,ESP1,color="#FCE7F3",alpha=0.55,zorder=0)
ax.axvline(ESP0,color=VERM,lw=1.0,ls=(0,(4,3)),zorder=5,ymax=LT)
ax.axvline(ESP1,color=VERM,lw=1.0,ls=(0,(4,3)),zorder=5,ymax=LT)
ax.text((ESP0+ESP1)/2,335,'ESPIN',fontsize=10,color=VERM,ha='center',va='bottom',fontweight='bold',zorder=6)
ax.annotate('',xy=(ESP1,300),xytext=(ESP0,300),arrowprops=dict(arrowstyle='<->',color=VERM,lw=1.1),zorder=6)
# números: +237, -294 (existentes) e -112, -137 (citados no patamar)
ax.text(idx(1990),var[idx(1990)]+14,'+237',ha='center',va='bottom',fontsize=11.5,fontweight='bold',color=PRETO)
ax.text(idx(2020),var[idx(2020)]-14,'−294',ha='center',va='top',fontsize=13,fontweight='bold',color=PRETO)
ax.text(idx(2024),var[idx(2024)]-34,'−112',ha='center',va='top',fontsize=11.5,fontweight='bold',color=PRETO)
ax.text(idx(2025),var[idx(2025)]-58,'−137',ha='center',va='top',fontsize=11.5,fontweight='bold',color=PRETO)
fig.text(0.02,0.965,'A variação anual revela 2020 como o fundo da retração',
         fontsize=13.5,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.915,'Variação anual do acervo de controle concentrado (distribuição menos baixa), 1988-2025',
         fontsize=10.5,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.86,bottom=0.10,left=0.03,right=0.99)
plt.savefig('../FINAL/1d_variacao_acervo_anual_1988-2025.png',facecolor='white'); plt.close()
print('1.c: +572/797/251 | 1.d: +237/-294/-112/-137 | pontilhados elevados')
import pandas as pd, numpy as np
from estilo import *
PRETO='#000000'
ac = pd.read_csv('/mnt/user-data/uploads/acervo_baixa_distribuicao.csv').sort_values('Ano').reset_index(drop=True)
anos = ac['Ano'].astype(int).tolist()
dist = ac['Total Distribuídos'].astype(int).tolist()
baix = ac['Total Baixas'].astype(int).tolist()
var  = [d-b for d,b in zip(dist,baix)]
def idx(a): return anos.index(a)
def pos_mes(ano,mes,dia=15): return idx(ano)-0.5+((mes-1)+(dia-1)/30)/12
ER=[(pos_mes(2016,6,22),'ER','51'),(pos_mes(2019,6,14),'ER','52'),(pos_mes(2020,3,18),'ER','53')]
ESP0=pos_mes(2020,2,3); ESP1=pos_mes(2022,4,22)

def marcadores(ax,ytop,esp_y,esp_lab_y):
    for pos,er,num in ER:
        ax.axvline(pos,color=PRETO,lw=1.0,ls=(0,(4,3)),zorder=5)
        ax.text(pos,ytop,er,fontsize=8.5,color=PRETO,ha='center',va='bottom',fontweight='bold',zorder=6)
        ax.text(pos,ytop-0.06*abs(ax.get_ylim()[1]-ax.get_ylim()[0]),num,fontsize=8.5,color=PRETO,ha='center',va='bottom',fontweight='bold',zorder=6)
    ax.axvspan(ESP0,ESP1,color="#FCE7F3",alpha=0.55,zorder=0)
    ax.axvline(ESP0,color=VERM,lw=1.0,ls=(0,(4,3)),zorder=5)
    ax.axvline(ESP1,color=VERM,lw=1.0,ls=(0,(4,3)),zorder=5)
    ax.annotate('',xy=(ESP1,esp_y),xytext=(ESP0,esp_y),arrowprops=dict(arrowstyle='<->',color=VERM,lw=1.0),zorder=6)
    ax.text((ESP0+ESP1)/2,esp_lab_y,'ESPIN',fontsize=8.5,color=VERM,ha='center',va='bottom',fontweight='bold',zorder=6)

# ===== 1.a trienal — SEM marcadores =====
tri_lab=['1988\n1990','1991\n1993','1994\n1996','1997\n1999','2000\n2002','2003\n2005','2006\n2008',
         '2009\n2011','2012\n2014','2015\n2017','2018\n2020','2021\n2023','2024\n2025*']
tri_val=[397,377,272,286,106,201,-28,222,173,351,-537,-540,-249]
fig,ax=base((10,4.8))
cores=[CINZA if v>=0 else VERM for v in tri_val]
b=ax.bar(range(len(tri_val)),tri_val,0.66,color=cores,zorder=3)
for r,v in zip(b,tri_val):
    ax.text(r.get_x()+r.get_width()/2,v+(18 if v>=0 else -18),f'{v:+d}'.replace('-','−'),
            ha='center',va='bottom' if v>=0 else 'top',fontsize=12,fontweight='bold',color=PRETO)
ax.axhline(0,color=PRETO,lw=1); ax.set_xticks(range(len(tri_val)))
ax.set_xticklabels(tri_lab,fontsize=9.5,color=PRETO,fontweight='bold'); ax.set_yticks([]); ax.set_ylim(-660,500)
ax.tick_params(colors=PRETO)
fig.text(0.02,0.955,'Após três décadas de acumulação, o acervo passa a encolher em 2018',
         fontsize=13,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.90,'Variação anual do acervo de controle concentrado, agregada por triênio, 1988-2025 (* biênio)',
         fontsize=10,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.82,bottom=0.13,left=0.03,right=0.98)
plt.savefig('../FINAL/1a_variacao_acervo_trienal_1988-2025.png',facecolor='white'); plt.close()

# ===== 1.c espelhado — COM marcadores =====
fig,ax=base((12,7.2))
x=np.arange(len(anos))
ax.bar(x,dist,0.8,color=AZUL,zorder=3,label='Distribuição')
ax.bar(x,[-b for b in baix],0.8,color=CINZA,zorder=3,label='Baixa')
ax.axhline(0,color=PRETO,lw=1)
ax.set_xticks(x); ax.set_xticklabels(anos,fontsize=9.5,color=PRETO,rotation=90,fontweight='bold')
ax.set_yticks([]); ax.tick_params(colors=PRETO)
ymax_d=int(max(dist)*1.30); ymin_d=-int(max(baix)*1.15)
ax.set_ylim(ymin_d,ymax_d)
for i,(d,b) in enumerate(zip(dist,baix)):
    ax.text(i,d+15,br(d),ha='center',va='bottom',fontsize=6.5,fontweight='bold',color=PRETO,zorder=6)
    ax.text(i,-b-15,br(b),ha='center',va='top',fontsize=6.5,fontweight='bold',color=PRETO,zorder=6)
er_ys=[ymax_d*0.92,ymax_d*0.80,ymax_d*0.68]
for pos,er,num,yl in zip([p for p,_,_ in ER],['ER','ER','ER'],['51','52','53'],er_ys):
    ax.axvline(pos,color=PRETO,lw=1.0,ls=(0,(4,3)),zorder=5)
    ax.text(pos,yl,er,fontsize=8.5,color=PRETO,ha='center',va='bottom',fontweight='bold',zorder=6)
    ax.text(pos,yl-0.06*(ymax_d-ymin_d),num,fontsize=8.5,color=PRETO,ha='center',va='bottom',fontweight='bold',zorder=6)
x0_esp=anos.index(2020)-0.5; x1_esp=anos.index(2022)+0.5
ax.axvspan(x0_esp,x1_esp,color=VERDE,alpha=0.35,zorder=0)
ax.axvline(x1_esp,color=VERM,lw=1.0,ls=(0,(4,3)),zorder=5)
esp_y=ymax_d*0.86
ax.text((x0_esp+x1_esp)/2,esp_y,'ESPIN',fontsize=8.5,color=VERM,ha='center',va='bottom',fontweight='bold',zorder=6)
ax.legend(frameon=False,fontsize=10.5,loc='lower left',labelcolor=PRETO)
fig.text(0.02,0.965,'A baixa supera a distribuição a partir de 2018',
         fontsize=13.5,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.915,'Distribuição (acima) e baixa (abaixo) de processos de controle concentrado, por ano, 1988-2025',
         fontsize=10.5,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.86,bottom=0.10,left=0.03,right=0.99)
plt.savefig('../FINAL/1c_distribuicao_baixa_espelhado_1988-2025.png',facecolor='white'); plt.close()

# ===== 1.d variação anual — COM marcadores =====
fig,ax=base((12,5.0))
cores=[CINZA if v>=0 else VERM for v in var]
ax.bar(x,var,0.8,color=cores,zorder=3)
ax.axhline(0,color=PRETO,lw=1)
ax.set_xticks(x); ax.set_xticklabels(anos,fontsize=9.5,color=PRETO,rotation=90,fontweight='bold')
ax.set_yticks([]); ax.set_ylim(-360,320); ax.tick_params(colors=PRETO)
for i,v in enumerate(var):
    if v in (min(var),max(var)):
        ax.text(i,v+(10 if v>=0 else -10),f'{v:+d}'.replace('-','−'),ha='center',
                va='bottom' if v>=0 else 'top',fontsize=9.5,fontweight='bold',color=PRETO)
marcadores(ax,285,215,230)
fig.text(0.02,0.965,'A variação anual revela 2020 como o fundo da retração',
         fontsize=13.5,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.915,'Variação anual do acervo de controle concentrado (distribuição menos baixa), 1988-2025',
         fontsize=10.5,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.86,bottom=0.10,left=0.03,right=0.99)
plt.savefig('../FINAL/1d_variacao_acervo_anual_1988-2025.png',facecolor='white'); plt.close()
print('1.a, 1.c, 1.d refeitos no padrão')
import pandas as pd, numpy as np
from estilo import *
PRETO='#000000'
df = pd.read_parquet('/mnt/user-data/uploads/inclusoes_em_pauta_mestre.parquet')
anos=list(range(2020,2026))
for amb,arq,tit in [('Plenário Virtual','2e_inclusoes_classe_ano_PV_2020-2025','Plenário Virtual'),
                    ('Plenário Físico','2f_inclusoes_classe_ano_PP_2020-2025','Plenário Presencial')]:
    g=df[df.ambiente==amb].groupby(['ano','classe']).size().unstack(fill_value=0)
    fig,ax=base((8.6,4.6))
    x=np.arange(6); w=0.2
    for i,(cl,cor) in enumerate([('ADI',AZUL),('ADPF',VERDE),('ADC',ROXO),('ADO',CINZA)]):
        vals=[int(g.loc[a,cl]) if cl in g.columns else 0 for a in anos]
        b=ax.bar(x+(i-1.5)*w,vals,w,color=cor,label=cl,zorder=3)
        for r in b:
            h=r.get_height()
            if h>0:
                ax.text(r.get_x()+r.get_width()/2,h+10,br(h),ha='center',fontsize=8,
                        fontweight='bold',color=PRETO)
    ax.set_xticks(x); ax.set_xticklabels(anos,fontsize=11,color=PRETO,fontweight='bold')
    ax.set_yticks([]); ax.set_ylim(0,860); ax.tick_params(colors=PRETO)
    ax.legend(frameon=False,fontsize=10,ncol=4,loc='upper right',labelcolor=PRETO)
    fig.text(0.02,0.955,f'Inclusões por classe e ano — {tit}',
             fontsize=13,fontweight='bold',color=PRETO,ha='left',va='top')
    fig.text(0.02,0.90,'Controle concentrado de constitucionalidade, 2020-2025',
             fontsize=10.5,color=PRETO,ha='left',va='top')
    plt.subplots_adjust(top=0.82,bottom=0.10,left=0.03,right=0.98)
    plt.savefig(f'../FINAL/{arq}.png',facecolor='white'); plt.close()
print('2.e e 2.f no padrão final, escala comum 0-860, com rótulos')
import numpy as np
from estilo import *
PRETO='#000000'
fig,ax=base((8,4.8))
tipos=['Principal','Recurso','Questão\nincidental']; x=np.arange(3); w=0.38
pv=[3383,1048,376]; pp=[2566,63,81]
b1=ax.bar(x-w/2,pv,w,color=AZUL,label='Plenário Virtual',zorder=3)
b2=ax.bar(x+w/2,pp,w,color=CINZA,label='Plenário Presencial',zorder=3)
for bars in (b1,b2):
    for r in bars:
        ax.text(r.get_x()+r.get_width()/2,r.get_height()+45,br(r.get_height()),
                ha='center',fontsize=11,fontweight='bold',color=PRETO)
ax.set_xticks(x); ax.set_xticklabels(tipos,fontsize=11.5,color=PRETO,fontweight='bold')
ax.set_yticks([]); ax.set_ylim(0,3750); ax.tick_params(colors=PRETO)
ax.legend(frameon=False,fontsize=10.5,loc='upper right',labelcolor=PRETO)
fig.text(0.02,0.955,'O recurso concentra-se no ambiente virtual; o principal, em ambos',
         fontsize=13,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.90,'Inclusões em pauta por tipo de questão e ambiente, 2020-2025',
         fontsize=10.5,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.82,bottom=0.10,left=0.03,right=0.98)
plt.savefig('../FINAL/2k2_tipo_questao_ambiente_2020-2025.png',facecolor='white'); plt.close()
print('2k2 no padrão novo')
import pandas as pd, numpy as np
from estilo import *
PRETO='#000000'
df = pd.read_parquet('/mnt/user-data/uploads/inclusoes_em_pauta_mestre.parquet')
anos=list(range(2020,2026))
sv,am,sp=[],[],[]
for a in anos:
    s=df[df.ano==a]
    pv=set(s[s.ambiente=='Plenário Virtual']['incidente'])
    pp=set(s[s.ambiente=='Plenário Físico']['incidente'])
    sv.append(len(pv-pp)); am.append(len(pv&pp)); sp.append(len(pp-pv))
print('Só Virtual:',sv); print('Ambos:',am); print('Só Presencial:',sp)

fig,ax=base((9,4.8))
x=np.arange(6); w=0.26
b1=ax.bar(x-w,sv,w,color=AZUL,label='Só Virtual',zorder=3)
b2=ax.bar(x,am,w,color=AZUL_CLARO,label='Ambos',zorder=3)
b3=ax.bar(x+w,sp,w,color=CINZA,label='Só Presencial',zorder=3)
for bars in (b1,b2,b3):
    for r in bars:
        ax.text(r.get_x()+r.get_width()/2,r.get_height()+8,br(r.get_height()),
                ha='center',fontsize=9.5,fontweight='bold',color=PRETO)
ax.set_xticks(x); ax.set_xticklabels(anos,fontsize=11,color=PRETO,fontweight='bold')
ax.set_yticks([]); ax.set_ylim(0,760); ax.tick_params(colors=PRETO)
ax.legend(frameon=False,fontsize=10.5,ncol=3,loc='upper right',labelcolor=PRETO)
fig.text(0.02,0.955,'A tramitação exclusivamente presencial torna-se residual',
         fontsize=13.5,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.90,'Processos por ano e tipo de tramitação, classificados dentro de cada ano, 2020-2025',
         fontsize=10.5,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.82,bottom=0.10,left=0.03,right=0.98)
plt.savefig('../FINAL/2h_tramitacao_anual_2020-2025.png',facecolor='white'); plt.close()
print('2.h gerado')
import numpy as np
from estilo import *
PRETO='#000000'

def tram(arq, titulo_txt, sub, vals, pcts, ilustrativo=False):
    fig,ax=base((8,3.6),bottom_axis=False)
    cats=['Somente\nvirtual','Ambos os\nambientes','Somente\npresencial']
    cores=[AZUL,AZUL_CLARO,CINZA]
    y=[2,1,0]
    if ilustrativo:
        vals_plot=[0.15,0.25,0.60]  # proporções fictícias só p/ forma
        b=ax.barh(y,vals_plot,0.6,color=cores,zorder=3)
        for yi in y:
            ax.text(vals_plot[2-yi]+0.02,yi,'___  (__%)',va='center',fontsize=12,
                    fontweight='bold',color=PRETO)
        ax.set_xlim(0,1.0)
        ax.text(0.5,1.0,'MODELO ILUSTRATIVO\naguarda dados 2016-2019',transform=ax.transAxes,
                ha='center',va='center',fontsize=18,color='#B91C1C',alpha=0.35,
                fontweight='bold',rotation=12,zorder=10)
    else:
        b=ax.barh(y,vals,0.6,color=cores,zorder=3)
        for yi in y:
            v=vals[2-yi]; p=pcts[2-yi]
            ax.text(v+30,yi,f'{br(v)}  ({br(p,1)}%)',va='center',fontsize=12,
                    fontweight='bold',color=PRETO)
        ax.set_xlim(0,2600)
    ax.set_yticks(y); ax.set_yticklabels(cats,fontsize=11.5,color=PRETO,fontweight='bold')
    ax.set_xticks([]); ax.tick_params(colors=PRETO)
    fig.text(0.02,0.955,titulo_txt,fontsize=13,fontweight='bold',color=PRETO,ha='left',va='top')
    fig.text(0.02,0.885,sub,fontsize=10,color=PRETO,ha='left',va='top')
    plt.subplots_adjust(top=0.78,bottom=0.05,left=0.16,right=0.97)
    plt.savefig(arq,facecolor='white'); plt.close()

tram('../FINAL/3.2_tramitacao_periodo_2020-2025.png',
     'Três de cada quatro processos nunca passam pelo presencial',
     'Processos de controle concentrado por tipo de tramitação, 2020-2025 (n=2.834)',
     [2197,478,159],[77.5,16.9,5.6])

tram('../MODELO_3.1_tramitacao_2016-2019.png',
     'MODELO do 3.1 — Tramitação por período, 2016-2019',
     'Mesmo formato do 3.2; barras e números entram quando o parquet do antes for regerado',
     None,None,ilustrativo=True)
print('3.2 real + modelo 3.1 gerados')
import pandas as pd, numpy as np
from estilo import *
PRETO='#000000'
df = pd.read_parquet('/home/claude/inclusoes_2016_2025_corrigido.parquet')
anos=list(range(2016,2026))
PVn='Plenário Virtual'; PPn='Plenário Físico'

# ---------- 2.a participação 2016-2025 ----------
part=[round(100*(df[df.ano==a]['ambiente'].eq(PVn)).mean(),1) for a in anos]
fig,ax=base((9.6,4.8))
b=ax.bar(range(10),part,0.62,color=AZUL,zorder=3)
for r,v in zip(b,part):
    ax.text(r.get_x()+r.get_width()/2,v+2,br(v,1)+'%',ha='center',fontsize=11,fontweight='bold',color=PRETO)
ax.set_xticks(range(10)); ax.set_xticklabels(anos,fontsize=10.5,color=PRETO,fontweight='bold')
ax.set_ylim(0,100); ax.set_yticks([]); ax.tick_params(colors=PRETO)
xe=6.45
ax.axvline(xe,color=VERM,ls=(0,(4,3)),lw=1.2,ymax=0.80)
ax.text(xe,84,'fim da ESPIN',ha='center',fontsize=9.5,color=VERM,fontweight='bold')
fig.text(0.02,0.955,'De 4% a dois terços da pauta: o degrau da universalização',
         fontsize=13.5,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.90,'Percentual das inclusões em pauta destinadas ao ambiente virtual, 2016-2025',
         fontsize=10.5,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.82,bottom=0.11,left=0.03,right=0.98)
plt.savefig('../FINAL/2016_2a_participacao_ano_2016-2025.png',facecolor='white'); plt.close()

# ---------- 2.b inclusões ano/ambiente ----------
pv=[int((df[(df.ano==a)&(df.ambiente==PVn)]).shape[0]) for a in anos]
pp=[int((df[(df.ano==a)&(df.ambiente==PPn)]).shape[0]) for a in anos]
fig,ax=base((10,4.8))
x=np.arange(10); w=0.4
b1=ax.bar(x-w/2,pv,w,color=AZUL,label='Plenário Virtual',zorder=3)
b2=ax.bar(x+w/2,pp,w,color=CINZA,label='Plenário Presencial',zorder=3)
for bars in (b1,b2):
    for r in bars:
        ax.text(r.get_x()+r.get_width()/2,r.get_height()+12,br(r.get_height()),ha='center',fontsize=8,fontweight='bold',color=PRETO)
ax.set_xticks(x); ax.set_xticklabels(anos,fontsize=10.5,color=PRETO,fontweight='bold')
ax.set_yticks([]); ax.set_ylim(0,1080); ax.tick_params(colors=PRETO)
ax.legend(frameon=False,fontsize=10.5,loc='upper left',labelcolor=PRETO)
fig.text(0.02,0.955,'O salto das inclusões no ambiente virtual',
         fontsize=13.5,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.90,'Inclusões em pauta por ano e ambiente, 2016-2025',fontsize=10.5,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.82,bottom=0.11,left=0.03,right=0.98)
plt.savefig('../FINAL/2016_2b_inclusoes_ano_ambiente_2016-2025.png',facecolor='white'); plt.close()

# ---------- 3.1 tramitação período 2016-2019 (real) ----------
antes=df[df.ano<=2019]
spv=set(antes[antes.ambiente==PVn]['incidente']); spp=set(antes[antes.ambiente==PPn]['incidente'])
sv,am,sp=len(spv-spp),len(spv&spp),len(spp-spv); tot=sv+am+sp
fig,ax=base((8,3.6),bottom_axis=False)
cats=['Somente\nvirtual','Ambos os\nambientes','Somente\npresencial']
vals=[sv,am,sp]; cores=[AZUL,AZUL_CLARO,CINZA]; y=[2,1,0]
ax.barh(y,vals,0.6,color=cores,zorder=3)
for yi in y:
    v=vals[2-yi]; p=100*v/tot
    ax.text(v+12,yi,f'{br(v)}  ({br(p,1)}%)',va='center',fontsize=12,fontweight='bold',color=PRETO)
ax.set_yticks(y); ax.set_yticklabels(cats,fontsize=11.5,color=PRETO,fontweight='bold')
ax.set_xticks([]); ax.set_xlim(0,2600); ax.tick_params(colors=PRETO)
fig.text(0.02,0.955,'Antes da universalização, o caminho era o presencial',
         fontsize=13,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.885,f'Processos de controle concentrado por tipo de tramitação, 2016-2019 (n={br(tot)})',
         fontsize=10,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.78,bottom=0.05,left=0.16,right=0.97)
plt.savefig('../FINAL/2016_3.1_tramitacao_periodo_2016-2019.png',facecolor='white'); plt.close()

# ---------- 2.i tramitação anual 2016-2025 ----------
sv_,am_,sp_=[],[],[]
for a in anos:
    s=df[df.ano==a]
    p1=set(s[s.ambiente==PVn]['incidente']); p2=set(s[s.ambiente==PPn]['incidente'])
    sv_.append(len(p1-p2)); am_.append(len(p1&p2)); sp_.append(len(p2-p1))
fig,ax=base((10.5,4.8))
w=0.26
b1=ax.bar(x-w,sv_,w,color=AZUL,label='Só Virtual',zorder=3)
b2=ax.bar(x,am_,w,color=AZUL_CLARO,label='Ambos',zorder=3)
b3=ax.bar(x+w,sp_,w,color=CINZA,label='Só Presencial',zorder=3)
for bars in (b1,b2,b3):
    for r in bars:
        h=r.get_height()
        if h>0: ax.text(r.get_x()+r.get_width()/2,h+8,br(h),ha='center',fontsize=7.5,fontweight='bold',color=PRETO)
ax.set_xticks(x); ax.set_xticklabels(anos,fontsize=10.5,color=PRETO,fontweight='bold')
ax.set_yticks([]); ax.set_ylim(0,760); ax.tick_params(colors=PRETO)
ax.legend(frameon=False,fontsize=10.5,ncol=3,loc='upper right',labelcolor=PRETO)
fig.text(0.02,0.955,'O cruzamento: o virtual ultrapassa o presencial em 2020',
         fontsize=13.5,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.90,'Processos por ano e tipo de tramitação, classificados dentro de cada ano, 2016-2025',
         fontsize=10.5,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.82,bottom=0.10,left=0.03,right=0.99)
plt.savefig('../FINAL/2016_2i_tramitacao_anual_2016-2025.png',facecolor='white'); plt.close()

# ---------- 2.c composição do PV por ano, 2016-2019 ----------
comp = df[(df.ano<=2019)&(df.ambiente==PVn)].groupby(['ano','tq']).size().unstack(fill_value=0)
fig,ax=base((8,4.4))
xa=np.arange(4); anos4=[2016,2017,2018,2019]
rc=[int(comp.loc[a].get('RC',0)) for a in anos4]
pr=[int(comp.loc[a].get('PR',0)) for a in anos4]
ij=[int(comp.loc[a].get('IJ',0)) for a in anos4]
ax.bar(xa,rc,0.55,color=VERDE,label='Recurso',zorder=3)
ax.bar(xa,pr,0.55,bottom=rc,color=AZUL,label='Principal',zorder=3)
ax.bar(xa,ij,0.55,bottom=[rc[i]+pr[i] for i in range(4)],color=CINZA,label='Questão incidental',zorder=3)
for i in range(4):
    tot_i=rc[i]+pr[i]+ij[i]
    ax.text(i,tot_i+10,br(tot_i),ha='center',fontsize=11,fontweight='bold',color=PRETO)
    if rc[i]>15: ax.text(i,rc[i]/2,br(rc[i]),ha='center',va='center',fontsize=10,fontweight='bold',color='white')
    if pr[i]>30: ax.text(i,rc[i]+pr[i]/2,br(pr[i]),ha='center',va='center',fontsize=10,fontweight='bold',color='white')
ax.set_xticks(xa); ax.set_xticklabels(anos4,fontsize=11,color=PRETO,fontweight='bold')
ax.set_yticks([]); ax.set_ylim(0,520); ax.tick_params(colors=PRETO)
ax.legend(frameon=False,fontsize=10,ncol=3,loc='upper left',labelcolor=PRETO)
fig.text(0.02,0.955,'Em 2019, o ambiente virtual deixa de ser exclusivamente recursal',
         fontsize=13,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.90,'Inclusões do Plenário Virtual por tipo de questão, 2016-2019',
         fontsize=10.5,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.82,bottom=0.10,left=0.03,right=0.98)
plt.savefig('../FINAL/2016_2c_composicao_PV_2016-2019.png',facecolor='white'); plt.close()

# ---------- 2.k1 tipo de questão por ambiente 2016-2019 ----------
ct = pd.crosstab(antes['ambiente'],antes['tq'])
fig,ax=base((8,4.6))
tipos=['Principal','Recurso','Questão\nincidental']; xt=np.arange(3); w=0.38
pvv=[int(ct.loc[PVn].get(k,0)) for k in ['PR','RC','IJ']]
ppv=[int(ct.loc[PPn].get(k,0)) for k in ['PR','RC','IJ']]
b1=ax.bar(xt-w/2,pvv,w,color=AZUL,label='Plenário Virtual',zorder=3)
b2=ax.bar(xt+w/2,ppv,w,color=CINZA,label='Plenário Presencial',zorder=3)
for bars in (b1,b2):
    for r in bars:
        ax.text(r.get_x()+r.get_width()/2,r.get_height()+25,br(r.get_height()),ha='center',fontsize=10.5,fontweight='bold',color=PRETO)
ax.set_xticks(xt); ax.set_xticklabels(tipos,fontsize=11.5,color=PRETO,fontweight='bold')
ax.set_yticks([]); ax.set_ylim(0,2150); ax.tick_params(colors=PRETO)
ax.legend(frameon=False,fontsize=10.5,loc='upper right',labelcolor=PRETO)
fig.text(0.02,0.955,'Antes da universalização, o mérito era do presencial; os recursos já migravam',
         fontsize=12.5,fontweight='bold',color=PRETO,ha='left',va='top')
fig.text(0.02,0.90,'Inclusões em pauta por tipo de questão e ambiente, 2016-2019',
         fontsize=10.5,color=PRETO,ha='left',va='top')
plt.subplots_adjust(top=0.82,bottom=0.10,left=0.03,right=0.98)
plt.savefig('../FINAL/2016_2k1_tipo_questao_ambiente_2016-2019.png',facecolor='white'); plt.close()
print('6 peças do antes geradas')
import pandas as pd, numpy as np
from estilo import *
df = pd.read_parquet('/mnt/user-data/uploads/inclusoes_em_pauta_mestre.parquet')
df['tq']=df['tipo_questao'].replace('Não identificado','PR')
anos=list(range(2020,2026))
PVn='Plenário Virtual'; PPn='Plenário Físico'

# 2.a participação por ano (2020-2025) — versão do NA sem o marco, será estendida depois
part=[round(100*(df[df.ano==a]['ambiente'].eq(PVn)).mean(),1) for a in anos]
fig,ax=base((8,4.6))
b=ax.bar(range(6),part,0.62,color=AZUL,zorder=3)
for r,v in zip(b,part):
    ax.text(r.get_x()+r.get_width()/2,v+2,br(v,1)+'%',ha='center',fontsize=12,fontweight='bold',color=ESC)
ax.set_xticks(range(6)); ax.set_xticklabels(anos,fontsize=11); ax.set_ylim(0,100); ax.set_yticks([])
xe=2+0.45
ax.axvline(xe,color=VERM,ls=(0,(4,3)),lw=1.3,ymax=0.82)
ax.text(xe,86,'fim da ESPIN\n(abr/2022)',ha='center',fontsize=9.5,color=VERM)
titulo(fig,'A participação do Plenário Virtual mantém-se entre 59% e 68% ao ano',
       'Percentual das inclusões em pauta destinadas ao ambiente virtual, 2020-2025')
fonte(fig)
plt.subplots_adjust(top=0.82,bottom=0.12,left=0.03,right=0.98)
plt.savefig('../G2a_participacao_ano.png',facecolor='white'); plt.close()

# 2.b inclusões por ano e ambiente
pv=[int((df[(df.ano==a)&(df.ambiente==PVn)]).shape[0]) for a in anos]
pp=[int((df[(df.ano==a)&(df.ambiente==PPn)]).shape[0]) for a in anos]
fig,ax=base((8.4,4.6))
x=np.arange(6); w=0.4
b1=ax.bar(x-w/2,pv,w,color=AZUL,label='Plenário Virtual',zorder=3)
b2=ax.bar(x+w/2,pp,w,color=CINZA,label='Plenário Presencial',zorder=3)
for bars in (b1,b2):
    for r in bars:
        ax.text(r.get_x()+r.get_width()/2,r.get_height()+12,br(r.get_height()),ha='center',fontsize=9,fontweight='bold',color=ESC)
ax.set_xticks(x); ax.set_xticklabels(anos,fontsize=11); ax.set_yticks([]); ax.set_ylim(0,1050)
ax.legend(frameon=False,fontsize=10,loc='upper right')
titulo(fig,'O ambiente virtual recebe a maior parte da pauta em todos os anos',
       'Inclusões em pauta por ano e ambiente, 2020-2025')
fonte(fig)
plt.subplots_adjust(top=0.82,bottom=0.11,left=0.03,right=0.98)
plt.savefig('../G2b_inclusoes_ano_ambiente.png',facecolor='white'); plt.close()

# 2.d/2.e classe por ano, cada ambiente, escala 0-800
for amb,nome,arq,tit in [(PVn,'Plenário Virtual','G2d','Plenário Virtual'),(PPn,'Plenário Presencial','G2e','Plenário Presencial')]:
    g=df[df.ambiente==amb].groupby(['ano','classe']).size().unstack(fill_value=0)
    fig,ax=base((8,4.4))
    x=np.arange(6); w=0.2
    for i,(cl,cor) in enumerate([('ADI',AZUL),('ADPF',VERDE),('ADC',ROXO),('ADO',CINZA)]):
        vals=[int(g.loc[a,cl]) if cl in g.columns else 0 for a in anos]
        ax.bar(x+(i-1.5)*w,vals,w,color=cor,label=cl,zorder=3)
    ax.set_xticks(x); ax.set_xticklabels(anos,fontsize=10.5); ax.set_yticks([]); ax.set_ylim(0,800)
    ax.legend(frameon=False,fontsize=9.5,ncol=4,loc='upper right')
    titulo(fig,f'Inclusões por classe e ano — {tit}','Controle concentrado, 2020-2025',fs=12)
    fonte(fig)
    plt.subplots_adjust(top=0.82,bottom=0.10,left=0.03,right=0.98)
    plt.savefig(f'../{arq}_classe_ano.png',facecolor='white'); plt.close()

# 2.f/2.g tramitação por período (só 2020-2025 aqui; 2016-2019 depende do "antes")
pv=set(df[df.ambiente==PVn]['incidente']); pp=set(df[df.ambiente==PPn]['incidente'])
sv,amb,sp=len(pv-pp),len(pv&pp),len(pp-pv); tot=sv+amb+sp
fig,ax=base((8,3.8),bottom_axis=False)
cats=['Somente\nvirtual','Ambos os\nambientes','Somente\npresencial']
vals=[sv,amb,sp]; pcts=[100*v/tot for v in vals]; cores=[AZUL,AZUL_CLARO,CINZA]
b=ax.barh([2,1,0],vals,0.6,color=cores,zorder=3)
for yi,(v,p) in enumerate(zip(reversed(vals),reversed(pcts))):
    vv=list(reversed(vals))[yi]; pp2=list(reversed(pcts))[yi]
    ax.text(vv+25,yi,f'{br(pp2,1)}%  ({br(vv)})',va='center',fontsize=11.5,fontweight='bold',color=ESC)
ax.set_yticks([2,1,0]); ax.set_yticklabels(cats,fontsize=11); ax.set_xlim(0,2500); ax.set_xticks([])
titulo(fig,'Três de cada quatro processos nunca passam pelo presencial',
       f'Processos de controle concentrado por tipo de tramitação, 2020-2025 (n={br(tot)})')
fonte(fig,'Unidade: processo.')
plt.subplots_adjust(top=0.80,bottom=0.06,left=0.14,right=0.97)
plt.savefig('../G2g_tramitacao_periodo_2020.png',facecolor='white'); plt.close()
print('Bloco 2 parte 1: participação, inclusões, classe(2), tramitação período')
import pandas as pd, numpy as np
from estilo import *
df = pd.read_parquet('/mnt/user-data/uploads/inclusoes_em_pauta_mestre.parquet')
df['tq']=df['tipo_questao'].replace('Não identificado','PR')
anos=list(range(2020,2026)); PVn='Plenário Virtual'; PPn='Plenário Físico'

# 2.i tipo de questão agrupado (absolutos)
pv=[3383,1048,376]; pp=[2566,63,81]
fig,ax=base((8,4.6))
tipos=['Principal','Recurso','Questão\nincidental']; x=np.arange(3); w=0.38
b1=ax.bar(x-w/2,pv,w,color=AZUL,label='Plenário Virtual',zorder=3)
b2=ax.bar(x+w/2,pp,w,color=CINZA,label='Plenário Presencial',zorder=3)
for bars in (b1,b2):
    for r in bars:
        ax.text(r.get_x()+r.get_width()/2,r.get_height()+40,br(r.get_height()),ha='center',fontsize=9.5,fontweight='bold',color=ESC)
ax.set_xticks(x); ax.set_xticklabels(tipos,fontsize=11); ax.set_yticks([]); ax.set_ylim(0,3700)
ax.legend(frameon=False,fontsize=10,loc='upper right')
titulo(fig,'O recurso concentra-se no ambiente virtual; o principal, em ambos',
       'Inclusões em pauta por tipo de questão e ambiente, 2020-2025')
fonte(fig)
plt.subplots_adjust(top=0.82,bottom=0.11,left=0.03,right=0.98)
plt.savefig('../G2i_tipo_questao.png',facecolor='white'); plt.close()

# 2.j recursos (ND)
fig,ax=base((8,3.2),bottom_axis=False)
ax.barh([0],[94.3],0.42,color=AZUL,zorder=3)
ax.barh([0],[5.7],0.42,left=[94.3],color=CINZA,zorder=3)
ax.text(94.3/2,0,'Plenário Virtual\n94,3%  (1.048)',ha='center',va='center',fontsize=12,fontweight='bold',color='white')
ax.text(101,0,'Presencial\n5,7% (63)',ha='left',va='center',fontsize=9.5,color=MED)
ax.set_xlim(0,118); ax.set_ylim(-0.6,0.6); ax.set_xticks([]); ax.set_yticks([])
titulo(fig,'A atividade recursal migrou quase toda para o ambiente virtual',
       'Destino das 1.111 inclusões de recursos (AgR, ED e afins), 2020-2025')
fonte(fig)
plt.subplots_adjust(top=0.74,bottom=0.05,left=0.03,right=0.97)
plt.savefig('../G2j_recursos.png',facecolor='white'); plt.close()

# 2.k pauta vs concluídos (NB)
fig,ax=base((8,4.6))
vals=[63.9,91.3]; b=ax.bar([0,1],vals,0.5,color=AZUL,zorder=3); b[0].set_alpha(0.55)
for r,v in zip(b,vals):
    ax.text(r.get_x()+r.get_width()/2,v+2.5,br(v,1)+'%',ha='center',fontsize=16,fontweight='bold',color=ESC)
ax.set_xticks([0,1]); ax.set_xticklabels(['Participação\nna pauta','Participação nos\njulgamentos concluídos'],fontsize=11.5)
ax.set_ylim(0,105); ax.set_yticks([]); ax.set_xlim(-0.55,1.55)
titulo(fig,'O Plenário Virtual concentra os julgamentos concluídos',
       'Participação do ambiente virtual na pauta e nos 3.187 julgamentos concluídos, 2020-2025')
fonte(fig)
plt.subplots_adjust(top=0.82,bottom=0.14,left=0.03,right=0.98)
plt.savefig('../G2k_pauta_concluidos.png',facecolor='white'); plt.close()

# 2.l/2.m desfecho por categoria e ano, escala 0-600
def desf(s):
    return {'Unânime':(s.desfecho=='Concluído - decisão unânime').sum(),
            'Maioria':(s.desfecho.isin(['Concluído - decisão maioria com o relator','Concluído - decisão maioria, vencido o relator'])).sum(),
            'Não concluído':(s.macro_desfecho!='Concluído').sum()}
for amb,arq,tit in [(PVn,'G2l','Plenário Virtual'),(PPn,'G2m','Plenário Presencial')]:
    fig,ax=base((8,4.4))
    x=np.arange(6); w=0.26
    cats=[('Unânime',VERDE),('Maioria',AZUL),('Não concluído',CINZA)]
    for i,(k,cor) in enumerate(cats):
        vals=[desf(df[(df.ambiente==amb)&(df.ano==a)])[k] for a in anos]
        ax.bar(x+(i-1)*w,vals,w,color=cor,label=k,zorder=3)
    ax.set_xticks(x); ax.set_xticklabels(anos,fontsize=10.5); ax.set_yticks([]); ax.set_ylim(0,600)
    ax.legend(frameon=False,fontsize=9.5,ncol=3,loc='upper right')
    titulo(fig,f'Desfecho por categoria e ano — {tit}','Inclusões em pauta, 2020-2025',fs=12)
    fonte(fig)
    plt.subplots_adjust(top=0.82,bottom=0.10,left=0.03,right=0.98)
    plt.savefig(f'../{arq}_desfecho_ano.png',facecolor='white'); plt.close()

# 2.o inclusões por processo (NE)
fig,ax=base((8,4.4))
vals=[1.8,4.3]; b=ax.bar([0,1],vals,0.45,color=[AZUL,CINZA],zorder=3)
for r,v in zip(b,vals):
    ax.text(r.get_x()+r.get_width()/2,v+0.12,br(v,1),ha='center',fontsize=16,fontweight='bold',color=ESC)
ax.set_xticks([0,1]); ax.set_xticklabels(['Plenário Virtual','Plenário Presencial'],fontsize=11.5)
ax.set_ylim(0,5); ax.set_yticks([]); ax.set_xlim(-0.55,1.55)
titulo(fig,'Cada julgamento presencial consome mais que o dobro de inclusões',
       'Média de inclusões em pauta por processo, por ambiente, 2020-2025')
fonte(fig)
plt.subplots_adjust(top=0.82,bottom=0.10,left=0.03,right=0.98)
plt.savefig('../G2o_inclusoes_processo.png',facecolor='white'); plt.close()

# 2.p conclusão por processo (NF)
fig,ax=base((8,4.4))
vals=[86.0,39.2]; b=ax.bar([0,1],vals,0.45,color=[AZUL,CINZA],zorder=3)
for r,v in zip(b,vals):
    ax.text(r.get_x()+r.get_width()/2,v+2.5,br(v,1)+'%',ha='center',fontsize=16,fontweight='bold',color=ESC)
ax.set_xticks([0,1]); ax.set_xticklabels(['Plenário Virtual','Plenário Presencial'],fontsize=11.5)
ax.set_ylim(0,100); ax.set_yticks([]); ax.set_xlim(-0.55,1.55)
titulo(fig,'Considerado o processo, o virtual conclui 86% do que pauta',
       'Percentual de processos pautados com julgamento concluído, 2020-2025')
fonte(fig,'Unidade: processo.')
plt.subplots_adjust(top=0.82,bottom=0.10,left=0.03,right=0.98)
plt.savefig('../G2p_conclusao_processo.png',facecolor='white'); plt.close()
print('Bloco 2 parte 2: tipo questão, recursos, pauta/concluídos, desfecho(2), incl/proc, concl/proc')
import pandas as pd, numpy as np
from estilo import *
df = pd.read_parquet('/mnt/user-data/uploads/inclusoes_em_pauta_mestre.parquet')
anos=list(range(2020,2026)); PVn='Plenário Virtual'; PPn='Plenário Físico'
nc=df[df.macro_desfecho!='Concluído']
def cats(s):
    return {'Pedido de vista':(s.desfecho=='Não concluído - pedido de vista').sum(),
            'Destaque':(s.desfecho=='Não concluído - destaque').sum(),
            'Retirado de pauta':(s.desfecho=='Não concluído - retirado de pauta').sum(),
            'Motivos diversos':(s.desfecho=='Não concluído - motivos diversos').sum()}
# escala comum
mx=0
for amb in [PVn,PPn]:
    for a in anos:
        mx=max(mx,max(cats(nc[(nc.ambiente==amb)&(nc.ano==a)]).values()))
ylim=(mx//50+1)*50
for amb,arq,tit in [(PVn,'G2o','Plenário Virtual'),(PPn,'G2p','Plenário Presencial')]:
    fig,ax=base((8.2,4.4))
    x=np.arange(6); w=0.2
    paleta=[('Pedido de vista',ROXO),('Destaque','#DB2777'),('Retirado de pauta','#F59E0B'),('Motivos diversos',CINZA)]
    for i,(k,cor) in enumerate(paleta):
        vals=[cats(nc[(nc.ambiente==amb)&(nc.ano==a)])[k] for a in anos]
        ax.bar(x+(i-1.5)*w,vals,w,color=cor,label=k,zorder=3)
    ax.set_xticks(x); ax.set_xticklabels(anos,fontsize=10.5); ax.set_yticks([]); ax.set_ylim(0,ylim)
    ax.legend(frameon=False,fontsize=9,ncol=4,loc='upper right')
    titulo(fig,f'Não concluídos por categoria e ano — {tit}','Inclusões em pauta, 2020-2025',fs=12)
    fonte(fig)
    plt.subplots_adjust(top=0.82,bottom=0.10,left=0.03,right=0.98)
    plt.savefig(f'../{arq}_nao_concluidos.png',facecolor='white'); plt.close()
print('escala comum:',ylim,'| 2 gráficos gerados')
