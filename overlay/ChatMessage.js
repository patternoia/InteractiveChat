let chatMessage = Vue.component('chat-message', {
    props: {
      raw: { default: '' },
      command: { default: '' },
      slideDir: { default: 'left' },
      useBttv: { default: true },
    },
    data() {
      return {
        show: true,
        badgeFragment: '',
        nameColor: '',
        displayName: '',
        messageBody: '',
      }
    },

    template: `
<div>
  <transition :name="'slide-'+slideDir">

    <div :style="lineStyle" v-if="show" class="chat-line__message">
      <span v-html="badgeFragment"></span>

      <span class="chat-line__username">
        <span>
          <span class="chat-author__display-name" :style="{ color: nameColor }">{{ displayName }}
          </span>
        </span>
      </span>
      <span>: </span>

      <span v-html="messageBody"></span>

    </div>

  </transition>
</div>
    `,

    beforeMount() {
      this.parseMessage(this.raw, this.command);
      if (this.useBttv) {
        this.messageBody = this.replaceBttv(this.messageBody);
      }
    },

    mounted() {
      let that = this;
      that.show = false;
      setTimeout(() => {
        that.$el.parentElement.removeChild(that.$el);
        that.$destroy();
      }, 15000);
    },

    computed: {
      lineStyle(asd, zxc) {
        if (this.slideDir === 'left')
          return {width:'100%', top: 0 + (Math.random() * (window.innerHeight-50))};

        return {};
      },
    },

    methods: {
      replaceBttv(html) {

        const limit = 5;
        let replaces = 0;
        let that = this;
        for (let emote of bttv) {
          if (replaces > limit)
            break;

          html = html.replace(new RegExp(emote.code, 'g'), (match, offset, string) => {
            replaces++;
            return emote.images ?
              that.ffzEmoteFragmentHtml(emote.id) :
              that.bttvEmoteFragmentHtml(emote.id);
          });
        }
        return html;
      },

      flatten(arr) {
        return [].concat.apply([], arr);
      },

      textFragmentHtml(text) {
        return `<span class="text-fragment">${text}</span>`
      },

      emoteFragmentHtml(emoteId) {
        return `
<div class="chat-line__message--emote-button"><span>
  <img class="chat-image chat-line__message--emote tw-inline-block" src="https://static-cdn.jtvnw.net/emoticons/v1/${emoteId}/1.0">
</span></div>
  `
      },

      bttvEmoteFragmentHtml(emoteId) {
        return `
<div class="bttv-emote-tooltip-wrapper bttv-emote bttv bttv-emo-${emoteId}">
  <img src="https://cdn.betterttv.net/emote/${emoteId}/1x" class="chat-line__message--emote">
</div>
  `
      },

      ffzEmoteFragmentHtml(emoteId) {
        return `
<div class="bttv-emote-tooltip-wrapper bttv-emote bttv bttv-emo-${emoteId}">
  <img src="https://cdn.betterttv.net/frankerfacez_emote/${emoteId}/1" class="chat-line__message--emote">
</div>
  `
      },

      badgeFragmentHtml(badge, version) {
        if (!badges.badge_sets[badge] || !badges.badge_sets[badge].versions[version]) {
          return '';
        }
        let src = badges.badge_sets[badge].versions[version].image_url_1x
        return `
<div class="tw-tooltip-wrapper tw-inline tw-relative">
  <img class="chat-badge bttv-chat-badge" src="${src}">
</div>
`
      },

      parseMessage(raw, command) {
        // basic parsing
        let divided = raw.slice(1).split('PRIVMSG');
        let message = divided[1].slice(divided[1].indexOf(':')+1);

        if (command.length && message.indexOf(command+' ') == 0) {
          message = message.slice(command.length+1);
        }

        let arr = divided[0].split(';');
        let obj = {};
        arr.map(el => Object.assign(obj, { [el.split("=")[0]] : el.split("=")[1]} ));
        if (!settings.ChannelId && Number(obj["room-id"])) {
          settings.ChannelId = obj["room-id"];
          fetchBadges();
          fetchBttv();
        }

        // fill emotes
        let emotes = []
        if (obj.emotes.length) {
          emotes = this.flatten(obj.emotes.split('/').map(el => {
            let splits = el.split(':')
            let id = splits[0];
            if (!splits[1])
              console.log(emoteArr);
            let ranges = splits[1].split(',');
            return ranges.map(r => ({i: id, s: Number(r.split('-')[0]), e: Number(r.split('-')[1])}))
          })).sort((a, b) => a.s - b.s);
        }

        // fill badges
        let badges = []
        if (obj.badges.length) {
          badges = obj.badges.split(',').map(b => b.split('/'));
        }

        this.nameColor = obj["color"]
        this.displayName = obj["display-name"]

        let html = '';

        // badges
        for (let badge of badges) {
          html += this.badgeFragmentHtml(badge[0], badge[1])
        }
        this.badgeFragment = html;

        // emotes and text
        html = ''
        if (!emotes.length) {
          html += this.textFragmentHtml(message);
        } else {
          let cursor = 0;
          for (let emote of emotes) {
            if (emote.s > cursor) {
              html += this.textFragmentHtml(message.substring(cursor, emote.s))
            }

            html += this.emoteFragmentHtml(emote.i)
            cursor = emote.e + 1;

          }

          if (message.length > cursor) {
            html += this.textFragmentHtml(message.substring(cursor, message.length))
          }
        }

        this.messageBody = html;
      },
    }
  })