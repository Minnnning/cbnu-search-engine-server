#!/bin/bash
set -e

# Elasticsearch 공식 엔트리포인트를 백그라운드에서 실행하고 PID 저장
/usr/local/bin/docker-entrypoint.sh eswrapper & 
ES_PID=$!

echo "Waiting for Elasticsearch to be available..."
# Elasticsearch가 완전히 기동될 때까지 충분히 대기
sleep 15

echo "Creating index 'notice_index'..."
curl -X PUT "http://localhost:9200/notice_index" \
     -H 'Content-Type: application/json' \
     -d'
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "nori_tokenizer_custom": {
          "type": "nori_tokenizer",
          "decompound_mode": "mixed",
          "discard_punctuation": "true"
        },
        "ngram_tokenizer": {
          "type": "ngram",
          "min_gram": 2,
          "max_gram": 3
        }
      },
      "filter": {
        "stopwords_filter": {
          "type": "stop",
          "stopwords": ["을", "를", "이", "가"]
        }
      },
      "analyzer": {
        "nori_analyzer": {
          "type": "custom",
          "tokenizer": "nori_tokenizer_custom",
          "filter": ["lowercase", "stopwords_filter", "nori_part_of_speech"],
          "char_filter": ["html_strip"]
        },
        "ngram_analyzer": {
          "type": "custom",
          "tokenizer": "ngram_tokenizer",
          "filter": ["lowercase", "stopwords_filter"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "integer"
      },
      "url": {
        "type": "keyword"
      },
      "title": {
        "type": "text",
        "analyzer": "nori_analyzer",
        "search_analyzer": "nori_analyzer",
        "fields": {
          "ngram": {
            "type": "text",
            "analyzer": "ngram_analyzer",
            "search_analyzer": "ngram_analyzer"
          }
        }
      },
      "content": {
        "type": "text",
        "analyzer": "nori_analyzer",
        "search_analyzer": "nori_analyzer",
        "fields": {
          "ngram": {
            "type": "text",
            "analyzer": "ngram_analyzer",
            "search_analyzer": "ngram_analyzer"
          }
        }
      },
      "category": {
        "type": "keyword"
      },
      "site": {
        "type": "keyword"
      },
      "date": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss"
      },
      "latitude": {
        "type": "double"
      },
      "longitude": {
        "type": "double"
      }
    }
  }
}'
echo "Index 'notice_index' created (if not existed)."

# ES 프로세스가 종료될 때까지 대기
wait $ES_PID
