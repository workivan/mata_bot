from aiogram import Bot
from dotenv import load_dotenv
import os

from app import storage as store

load_dotenv()
DEBUG = False
SUPER_USER_LOGIN = 'fv_sergey'
SUPER_USER_ID = 703619442
SUPER_USER_NICKNAME = 'Сергей Босс'
TOKEN = os.getenv("BOT_TOKEN")
PASSWORD = 'Мята'
PIN_MESSAGE = 'Закрепленное сообщение'
bot = Bot(token=TOKEN)

if DEBUG:
    USERS = dict()
else:
    USERS = store.UserStorage()

FIL = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]

REGEX = r"(?P<domain>\w+\.\w{2,3})"
FILTER_LIST = ['архипиздрит', 'басран', 'бздение', 'бздеть', 'блять', 'бздех', 'бзднуть', 'бля', 'бздун', 'бздунья',
               'бздюха',
               'бикса', 'блежник', 'блудилище', 'бляд', 'блябу', 'блябуду', 'блядун', 'блядунья', 'блядь', 'блядюга',
               'взьебка', 'волосянка', 'взьебывать', "взъебывать", 'выблядок', 'выблядыш', 'выебать', 'выеть',
               'выпердеть', 'высраться', 'выссаться', 'говенка', 'говенный', 'говешка', 'говназия', 'говнецо',
               'говно', 'говноед', 'говночист', 'говнюк', 'говнюха', 'говнядина', 'говняк', 'говняный', 'говнять',
               'гондон', 'дермо', 'долбоеб', 'дрисня', 'дрист', 'дристать', 'дристануть', 'дристун', 'дристуха',
               'дрочена', 'дрочила', 'дрочилка', 'дрочить', 'дрочка', 'ебало', 'ебальник', 'ебануть', 'ебаный', 'ебарь',
               'ебатория', 'ебать', 'ебаться', 'ебец', 'ебливый', 'ебля', 'ебнуть', 'ебнуться', 'ебня', 'ебун', 'елда',
               'елдак', 'елдачить', 'заговнять', 'задристать', 'задрока', 'заеба', 'заебанец', 'заебать', 'заебаться',
               'заебываться', 'заеть', 'залупа', 'залупаться', 'залупить', 'залупиться', 'замудохаться', 'засерун',
               'засеря', 'засерать', 'засирать', 'засранец', 'засрун', 'захуячить', 'злоебучий', 'изговнять',
               'изговняться', 'кляпыжиться', 'курва', 'курвенок', 'курвин', 'курвяжник', 'курвяжница', 'курвяжный',
               'манда', 'мандавошка', 'мандей', 'мандеть', 'мандища', 'мандюк', 'минет', 'минетчик', 'минетчица',
               'мокрохвостка', 'мокрощелка', 'мудак', 'муде', 'мудеть', 'мудила', 'мудистый', 'мудня', 'мудоеб',
               'мудозвон', 'муйня', 'набздеть', 'наговнять', 'надристать', 'надрочить', 'наебать', 'наебнуться',
               'наебывать', 'нассать', 'нахезать', 'нахуйник', 'насцать', 'обдристаться', 'обдристаться', 'обосранец',
               'обосрать', 'обосцать', 'обосцаться', 'обсирать', 'опизде', 'отпиздячить', 'отпороть', 'отъеть',
               'охуевательский', 'охуевать', 'охуевающий', 'охуеть', 'охуительный', 'охуячивать', 'охуячить', 'педрик',
               'пердеж', 'пердение', 'пердеть', 'пердильник', 'перднуть', 'пердун', 'пердунец', 'пердунина', 'пердунья',
               'пердуха', 'пердь', 'передок', 'пернуть', 'пидор', 'пизда', 'пиздануть', 'пизденка', 'пиздеть',
               'пиздить', 'пиздища', 'пиздобратия', 'пиздоватый', 'пиздорванец', 'пиздорванка', 'пиздострадатель',
               'пиздун', 'пиздюга', 'пиздюк', 'пиздячить', 'писять', 'питишка', 'плеха', 'подговнять', 'подъебнуться',
               'поебать', 'поеть', 'попысать', 'посрать', 'поставить', 'поцоватый', 'презерватив', 'проблядь',
               'проебать', 'промандеть', 'промудеть', 'пропиздеть', 'пропиздячить', 'пысать', 'разъеба', 'разъебай',
               'распиздай', 'распиздеться', 'распиздяй', 'распроеть', 'растыка', 'сговнять', 'секель', 'серун',
               'серька', 'сика', 'сикать', 'сикель', 'сирать', 'сирывать', 'скурвиться', 'скуреха', 'скурея', 'скуряга',
               'скуряжничать', 'спиздить', 'срака', 'сраный', 'сранье', 'срать', 'срун', 'ссака', 'ссаки', 'ссать',
               'старпер', 'струк', 'суходрочка', 'сцавинье', 'сцака', 'сцаки', 'сцание', 'сцать', 'сциха', 'сцуль',
               'сцыха', 'сыкун', 'титечка', 'титечный', 'титка', 'титочка', 'титька', 'трипер', 'триппер', 'уеть',
               'усраться', 'усцаться', 'фик', 'фуй', 'хезать', 'хер', 'херня', 'херовина', 'херовый', 'хитрожопый',
               'хлюха', 'хуевина', 'хуевый', 'хуек', 'хуепромышленник', 'хуерик', 'хуесос', 'хуище', 'хуй', 'хуйня',
               'хуйрик', 'хуякать', 'хуякнуть', 'целка', 'шлюха', 'сука', 'шлюшка', 'сучка', 'уебан', 'уебище',
               'долбаеб', 'долбаёб', 'пидр', 'пиздюк', 'пиздец', 'нах', 'нахуй', 'похуй', 'пизде', 'хую', 'говнарь',
               '6ля', '6лядь', '6лять', 'b3ъeб', 'cock', 'cunt', 'e6aль', 'ebal', 'eblan', 'eбaл', 'eбaть', 'eбyч',
               'eбать', 'eбёт', 'eблантий', 'fuck', 'fucker', 'fucking', 'xyёв', 'xyй', 'xyя', 'xуе', 'xуй', 'xую',
               'zaeb', 'zaebal', 'zaebali', 'zaebat', 'архипиздрит', 'ахуел', 'ахуеть', 'бздение', 'бздеть', 'бздех',
               'бздецы', 'бздит', 'бздицы', 'бздло', 'бзднуть', 'бздун', 'бздунья', 'бздюха', 'бздюшка', 'бздюшко',
               'бля', 'блябу', 'блябуду', 'бляд', 'бляди', 'блядина', 'блядище', 'блядки', 'блядовать', 'блядство',
               'блядун', 'блядуны', 'блядунья', 'блядь', 'блядюга', 'блять', 'вафел', 'вафлёр', 'взъебка', 'взьебка',
               'взьебывать', 'въеб', 'въебался', 'въебенн', 'въебусь', 'въебывать', 'выблядок', 'выблядыш', 'выеб',
               'выебать', 'выебен', 'выебнулся', 'выебон', 'выебываться', 'выпердеть', 'высраться', 'выссаться',
               'вьебен', 'гавно', 'гавнюк', 'гавнючка', 'гамно', 'гандон', 'гнид', 'гнида', 'гниды', 'говенка',
               'говенный', 'говешка', 'говназия', 'говнецо', 'говнище', 'говно', 'говноед', 'говнолинк', 'говночист',
               'говнюк', 'говнюха', 'говнядина', 'говняк', 'говняный', 'говнять', 'гондон', 'доебываться', 'долбоеб',
               'долбоёб', 'долбоящер', 'дрисня', 'дрист', 'дристануть', 'дристать', 'дристун', 'дристуха', 'дрочелло',
               'дрочена', 'дрочила', 'дрочилка', 'дрочистый', 'дрочить', 'дрочка', 'дрочун', 'е6ал', 'е6ут',
               'ебтвоюмать', 'ёбтвоюмать', 'ёбaн', 'ебaть', 'ебyч', 'ебал', 'ебало', 'ебальник', 'ебан', 'ебанамать',
               'ебанат', 'ебаная', 'ёбаная', 'ебанический', 'ебанный', 'ебанныйврот', 'ебаное', 'ебануть', 'ебануться',
               'ёбаную', 'ебаный', 'ебанько', 'ебарь', 'ебат', 'ёбат', 'ебатория', 'ебать', 'ебать-копать', 'ебаться',
               'ебашить', 'ебёна', 'ебет', 'ебёт', 'ебец', 'ебик', 'ебин', 'ебись', 'ебическая', 'ебки', 'ебла',
               'еблан', 'ебливый', 'еблище', 'ебло', 'еблыст', 'ебля', 'ёбн', 'ебнуть', 'ебнуться', 'ебня', 'ебошить',
               'ебская', 'ебский', 'ебтвоюмать', 'ебун', 'ебут', 'ебуч', 'ебуче', 'ебучее', 'ебучий', 'ебучим', 'ебущ',
               'ебырь', 'елда', 'елдак', 'елдачить', 'жопа', 'жопу', 'заговнять', 'задрачивать', 'задристать',
               'задрота', 'зае6', 'заё6', 'заеб', 'заёб', 'заеба', 'заебал', 'заебанец', 'заебастая', 'заебастый',
               'заебать', 'заебаться', 'заебашить', 'заебистое', 'заёбистое', 'заебистые', 'заёбистые', 'заебистый',
               'заёбистый', 'заебись', 'заебошить', 'заебываться', 'залуп', 'залупа', 'залупаться', 'залупить',
               'залупиться', 'замудохаться', 'запиздячить', 'засерать', 'засерун', 'засеря', 'засирать', 'засрун',
               'захуячить', 'заябестая', 'злоеб', 'злоебучая', 'злоебучее', 'злоебучий', 'ибанамат', 'ибонех',
               'изговнять', 'изговняться', 'изъебнуться', 'ипать', 'ипаться', 'ипаццо', 'Какдвапальцаобоссать', 'конча',
               'курва', 'курвятник', 'лох', 'лошарa', 'лошара', 'лошары', 'лошок', 'лярва', 'малафья', 'манда',
               'мандавошек', 'мандавошка', 'мандавошки', 'мандей', 'мандень', 'мандеть', 'мандища', 'мандой', 'манду',
               'мандюк', 'минет', 'минетчик', 'минетчица', 'млять', 'мокрощелка', 'мокрощёлка', 'мразь', 'мудak',
               'мудaк', 'мудаг', 'мудак', 'муде', 'мудель', 'мудеть', 'муди', 'мудил', 'мудила', 'мудистый', 'мудня',
               'мудоеб', 'мудозвон', 'мудоклюй', 'нахер', 'нахуй', 'набздел', 'набздеть', 'наговнять', 'надристать',
               'надрочить', 'наебать', 'наебет', 'наебнуть', 'наебнуться', 'наебывать', 'напиздел', 'напиздели',
               'напиздело', 'напиздили', 'насрать', 'настопиздить', 'нахер', 'нахрен', 'нахуй', 'нахуйник', 'неебет',
               'неебёт', 'невротебучий', 'невъебенно', 'нехира', 'нехрен', 'Нехуй', 'нехуйственно', 'ниибацо',
               'ниипацца', 'ниипаццо', 'ниипет', 'никуя', 'нихера', 'нихуя', 'обдристаться', 'обосранец', 'обосрать',
               'обосцать', 'обосцаться', 'обсирать', 'объебос', 'обьебатьобьебос', 'однохуйственно', 'опездал',
               'опизде', 'опизденивающе', 'остоебенить', 'остопиздеть', 'отмудохать', 'отпиздить', 'отпиздячить',
               'отпороть', 'отъебись', 'охуевательский', 'охуевать', 'охуевающий', 'охуел', 'охуенно', 'охуеньчик',
               'охуеть', 'охуительно', 'охуительный', 'охуяньчик', 'охуячивать', 'охуячить', 'очкун', 'падла',
               'падонки', 'падонок', 'паскуда', 'педерас', 'педик', 'педрик', 'педрила', 'педрилло', 'педрило',
               'педрилы', 'пездень', 'пездит', 'пездишь', 'пездо', 'пездят', 'пердануть', 'пердеж', 'пердение',
               'пердеть', 'пердильник', 'перднуть', 'пёрднуть', 'пердун', 'пердунец', 'пердунина', 'пердунья',
               'пердуха', 'пердь', 'переёбок', 'пернуть', 'пёрнуть', 'пи3д', 'пи3де', 'пи3ду', 'пиzдец', 'пидар',
               'пидарaс', 'пидарас', 'пидарасы', 'пидары', 'пидор', 'пидорасы', 'пидорка', 'пидорок', 'пидоры',
               'пидрас', 'пизда', 'пиздануть', 'пиздануться', 'пиздарваньчик', 'пиздато', 'пиздатое', 'пиздатый',
               'пизденка', 'пизденыш', 'пиздёныш', 'пиздеть', 'пиздец', 'пиздит', 'пиздить', 'пиздиться', 'пиздишь',
               'пиздища', 'пиздище', 'пиздобол', 'пиздоболы', 'пиздобратия', 'пиздоватая', 'пиздоватый', 'пиздолиз',
               'пиздонутые', 'пиздорванец', 'пиздорванка', 'пиздострадатель', 'пизду', 'пиздуй', 'пиздун', 'пиздунья',
               'пизды', 'пиздюга', 'пиздюк', 'пиздюлина', 'пиздюля', 'пиздят', 'пиздячить', 'писбшки', 'писька',
               'писькострадатель', 'писюн', 'писюшка', 'похуй', 'похую', 'подговнять', 'подонки', 'подонок',
               'подъебнуть', 'подъебнуться', 'поебать', 'поебень', 'поёбываает', 'поскуда', 'посрать', 'потаскуха',
               'потаскушка', 'похер', 'похерил', 'похерила', 'похерили', 'похеру', 'похрен', 'похрену', 'похуй',
               'похуист', 'похуистка', 'похую', 'придурок', 'приебаться', 'припиздень', 'припизднутый', 'припиздюлина',
               'пробзделся', 'проблядь', 'проеб', 'проебанка', 'проебать', 'промандеть', 'промудеть', 'пропизделся',
               'пропиздеть', 'пропиздячить', 'раздолбай', 'разхуячить', 'разъеб', 'разъеба', 'разъебай', 'разъебать',
               'распиздай', 'распиздеться', 'распиздяй', 'распиздяйство', 'распроеть', 'сволота', 'сволочь', 'сговнять',
               'секель', 'серун', 'серька', 'сестроеб', 'сикель', 'сила', 'сирать', 'сирывать', 'соси', 'спиздел',
               'спиздеть', 'спиздил', 'спиздила', 'спиздили', 'спиздит', 'спиздить', 'срака', 'сраку', 'сраный',
               'сранье', 'срать', 'срун', 'ссака', 'ссышь', 'стерва', 'страхопиздище', 'сука', 'суки', 'суходрочка',
               'сучара', 'сучий', 'сучка', 'сучко', 'сучонок', 'сучье', 'сцание', 'сцать', 'сцука', 'сцуки', 'сцуконах',
               'сцуль', 'сцыха', 'сцышь', 'съебаться', 'сыкун', 'трахае6', 'трахаеб', 'трахаёб', 'трахатель', 'ублюдок',
               'уебать', 'уёбища', 'уебище', 'уёбище', 'уебищное', 'уёбищное', 'уебк', 'уебки', 'уёбки', 'уебок',
               'уёбок', 'урюк', 'усраться', 'ушлепок', 'х_у_я_р_а', 'хyё', 'хyй', 'хyйня', 'хамло', 'хер', 'херня',
               'херовато', 'херовина', 'херовый', 'хитровыебанный', 'хитрожопый', 'хуeм', 'хуе', 'хуё', 'хуевато',
               'хуёвенький', 'хуевина', 'хуево', 'хуевый', 'хуёвый', 'хуек', 'хуёк', 'хуел', 'хуем', 'хуенч', 'хуеныш',
               'хуенький', 'хуеплет', 'хуеплёт', 'хуепромышленник', 'хуерик', 'хуерыло', 'хуесос', 'хуесоска', 'хуета',
               'хуетень', 'хуею', 'хуи', 'хуй', 'хуйком', 'хуйло', 'хуйня', 'хуйрик', 'хуище', 'хуля', 'хую', 'хуюл',
               'хуя', 'хуяк', 'хуякать', 'хуякнуть', 'хуяра', 'хуясе', 'хуячить', 'целка', 'чмо', 'чмошник', 'чмырь',
               'шалава', 'шалавой', 'шараёбиться', 'шлюха', 'шлюхой', 'шлюшка', 'ябывает']
