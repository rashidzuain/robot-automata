import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const output=path.dirname(fileURLToPath(import.meta.url));
const parts=[];
const colors={gnd:'#263344',power:'#dc3b42',logic:'#d0700b',ena:'#1465cc',in1:'#008375',in2:'#7d40b6'};
function text(x,y,t,size=20,anchor='start',color='#263344',weight=400){parts.push(`<text x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}" fill="${color}" font-weight="${weight}">${t}</text>`);}
function rect(x,y,w,h,fill,stroke='#bcc7d1',r=10){parts.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${stroke}" rx="${r}"/>`);}
function wire(d,c,width=5){parts.push(`<path d="${d}" fill="none" stroke="${c}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round"/>`);}
function dot(x,y,c){parts.push(`<circle cx="${x}" cy="${y}" r="6" fill="${c}"/>`);}
function port(x,y){parts.push(`<circle cx="${x}" cy="${y}" r="5" fill="white" stroke="#263344" stroke-width="2"/>`);}
function screw(x,y){parts.push(`<circle cx="${x}" cy="${y}" r="11" fill="#d9e4ed" stroke="#637887"/><path d="M${x-5},${y+5}l10,-10" stroke="#637887" stroke-width="2"/>`);}
function bridge(x,y,c){wire(`M${x-10},${y}h20`,'#ffffff',12);wire(`M${x-10},${y}Q${x},${y-16} ${x+10},${y}`,c);}
parts.push('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1240 990" width="1240" height="990"><title>Montaje de prueba con un motor: Arduino UNO, L298N, cuatro AA y resistencia de 10 kiloohmios</title><rect width="1240" height="990" fill="#fff"/><g font-family="Segoe UI,Arial,sans-serif">');
text(45,50,'Dibujo del montaje · UN motor',32,'start','#183954',600);
text(45,85,'Vista simplificada: seguí los nombres de los pines, no su posición en este dibujo.',19);
// Component bodies.
rect(60,280,225,412,'#def2f2','#178781',16);text(172,320,'Arduino UNO',25,'middle','#165c59',600);
rect(80,340,44,48,'#d7e1e6','#708492',3);text(102,414,'USB',18,'middle');
rect(90,472,45,114,'#364650','#24313c',3);for(let i=0;i<8;i++){wire(`M83,${483+i*13}h8`,'#849ba3',2);wire(`M135,${483+i*13}h8`,'#849ba3',2);}
wire('M80,364H45V224H175','#879aa5',7);text(187,231,'USB a la laptop',20);
rect(710,280,245,412,'#fde5e5','#b64545',12);text(832,321,'L298N',27,'middle','#8b2828',600);
rect(790,339,140,66,'#35404b','#1a2530',3);for(let i=0;i<7;i++)wire(`M${799+i*19},346v52`,'#74808c',4);
rect(765,536,43,43,'#e1e5e8','#6d7680',20);rect(874,594,43,43,'#e1e5e8','#6d7680',20);
text(440,163,'Puentes 5V-EN y ENA retirados',20,'middle','#8b2828',600);
text(440,193,'Pin +5V vecino de ENA: libre',19,'middle');
// Battery case, terminals are outside the pack drawing.
rect(740,120,350,111,'#29333e','#131c27',10);
for(let i=0;i<4;i++){rect(757+i*80,133,68,78,'#ca7035','#e0a46b',9);rect(761+i*80,155,60,47,'#343f48','#343f48',3);text(791+i*80,185,'AA',20,'middle','#fff');}
text(917,258,'4 AA · pack medido: 6,03 V',20,'middle');
// Motor with gearbox, wheel and separate terminals.
rect(1040,350,77,160,'#252d35','#111c25',12);for(let i=0;i<8;i++)wire(`M1046,${362+i*18}h65`,'#5b6770',3);
rect(1118,390,74,85,'#ffe17b','#b98c20',9);rect(1124,373,61,34,'#d4dde4','#7d909e',5);
text(1120,546,'Motor TT',22,'middle');text(1120,574,'3–6 V',21,'middle');
// Battery positive goes to motor-supply terminal. Ground returns avoid board interiors.
wire('M1062,231V280H1000V798H906V692',colors.power);port(906,692);text(885,672,'12V',21,'end',colors.power,600);text(1075,243,'+',22,'start',colors.power);
wire('M768,231V241H30V834H700',colors.gnd);text(746,232,'−',22);text(47,821,'Negativo de pilas',20);dot(325,834,colors.gnd);dot(548,834,colors.gnd);
wire('M285,657H325V834',colors.gnd);wire('M710,657H700V834',colors.gnd);dot(700,834,colors.gnd);
// Pulldown resistor, isolated from all crossing signal wires.
wire('M468,367V386',colors.gnd);rect(459,386,18,40,'#f3e7cd','#6c5b44',3);wire('M468,426V432H548V834',colors.gnd);text(448,414,'10 kΩ',20,'end');dot(468,367,colors.ena);
// Control wires.
const signals=[['D5','ENA',367,colors.ena],['D7','IN1',461,colors.in1],['D8','IN2',505,colors.in2],['5V','+5V',607,colors.logic]];
for(const [uno,driver,y,c] of signals){wire(`M285,${y}H710`,c);if(y>432)bridge(548,y,c);port(285,y);port(710,y);text(270,y+7,uno,22,'end',c,600);text(721,y+7,driver,21,'start',c,600);}
dot(468,367,colors.ena);text(431,351,'unión',18,'middle');
text(431,290,'D5 + ENA + resistencia',20,'middle');text(431,317,'se unen en la protoboard',18,'middle');
port(285,657);port(710,657);text(270,664,'GND',21,'end');text(721,664,'GND',21);
text(548,872,'GND común: todos estos cables negros están unidos',22,'middle');
// Motor output terminal block and wires. Neither is a fixed ground.
rect(929,432,50,85,'#3c92bd','#23658a',5);screw(953,453);screw(953,496);
wire('M978,453H1009V340H1140V373','#326ab1');bridge(997,453,'#326ab1');wire('M978,496H1027V322H1170V373','#894fb4');bridge(1000,496,'#894fb4');port(1140,373);port(1170,373);
text(917,460,'OUT1',20,'end');text(917,503,'OUT2',20,'end');
text(1119,622,'Un cable en cada OUT.',17,'middle');text(1119,648,'Ninguno a GND.',17,'middle');
text(45,924,'● Unión de cables      Arco en un cruce = cables que no se tocan',20);
text(45,957,'Armá el cableado con USB y pilas desconectados. Las ruedas quedan levantadas para la prueba.',20);
parts.push('</g></svg>');
await fs.writeFile(path.join(output,'dibujo-montaje-un-motor.svg'),parts.join('\n'),'utf8');
console.log('Dibujo de montaje guardado.');
