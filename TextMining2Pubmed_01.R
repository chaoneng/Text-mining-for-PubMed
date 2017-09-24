library(dplyr)
library(tidytext)

#自動斷詞
text_df %>%
  unnest_tokens(word, text)

##Tidying the works of Jane Austen
require(pubmed.mineR)
abstracts <- readabs("~/desktop/pubmed_result.txt")
abstracts@Abstract

text_df <- data_frame(text = abstracts@Abstract)
text_df

text_df %>%
  unnest_tokens(word, text)

text_df %>% 
  unnest_tokens(word, text) %>%    # split words
  anti_join(stop_words) %>%    # take out "a", "an", "the", etc.
  count(word, sort = TRUE)    # count occurrences
  

library(ggplot2)

text_df %>%
  unnest_tokens(word, text) %>%    # split words
  anti_join(stop_words) %>% 
  count(word, sort = TRUE) %>%
  filter(n > 10) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(word, n)) +
  geom_col() +
  xlab(NULL) +
  coord_flip()

##topicmodels

text_df %>% 
  unnest_tokens(word, text) %>%    # split words
  anti_join(stop_words) %>%    # take out "a", "an", "the", etc.
  count(word, sort = TRUE)    # count occurrences

desc_dtm <- text_df %>%
  unnest_tokens(word, text) %>%    # split words
  anti_join(stop_words) %>%    # take out "a", "an", "the", etc.
  count(line, word, sort = TRUE) %>%
  ungroup() %>%
  cast_dtm(line, word, n)

library(topicmodels)
desc_lda <- LDA(desc_dtm, k = 20, control = list(seed = 42))
tidy_lda <- tidy(desc_lda)

top_terms <- tidy_lda %>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  arrange(topic, -beta)

top_terms %>%
  mutate(term = reorder(term, beta)) %>%
  group_by(topic, term) %>%    
  arrange(desc(beta)) %>%  
  ungroup() %>%
  mutate(term = factor(paste(term, topic, sep = "__"), 
                       levels = rev(paste(term, topic, sep = "__")))) %>%
  ggplot(aes(term, beta, fill = as.factor(topic))) +
  geom_col(show.legend = FALSE) +
  coord_flip() +
  scale_x_discrete(labels = function(x) gsub("__.+$", "", x)) +
  labs(title = "Top 10 terms in each LDA topic",
       x = NULL, y = expression(beta)) +
  facet_wrap(~ topic, ncol = 5, scales = "free")

## Semantic analysis
contributions <- text_df %>%
  unnest_tokens(word, text) %>%    # split words
  anti_join(stop_words) %>%    # take out "a", "an", "the", etc.
  count(word, sort = TRUE) %>%
  inner_join(get_sentiments("afinn"), by = "word") %>%
  group_by(word) %>%
  summarize(occurences = n(),
            contribution = sum(score))

contributions %>%
  top_n(25, abs(contribution)) %>%
  mutate(word = reorder(word, contribution)) %>%
  ggplot(aes(word, contribution, fill = contribution > 0)) +
  geom_col(show.legend = FALSE) +
  coord_flip()

##Tokenizing by n-gram
library(dplyr)
library(tidytext)
library(janeaustenr)

text_df %>% 
  unnest_tokens(word, text, token = "ngrams", n = 2)

text_df %>%
  unnest_tokens(word, text, token = "ngrams", n = 2)%>%
  count(word, sort = TRUE)

library(tidyr)
text_separated <- text_df %>%
  unnest_tokens(word, text, token = "ngrams", n = 2)%>%
  separate(word, c("word1", "word2"), sep = " ")

text_filtered <- text_separated %>%
  filter(!word1 %in% stop_words$word) %>%
  filter(!word2 %in% stop_words$word)

# new bigram counts:
text_counts <- text_filtered %>% 
  count(word1, word2, sort = TRUE)

text_counts

##
text_united <- text_filtered %>%
  unite(tt, word1, word2, sep = " ")

text_united

##高频词
library(stringr)
wordf <- text_df %>%
  mutate(line = 1:nrow(text_df)) %>%
  filter(nchar(text) > 0) %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words) %>%
  filter(str_detect(word, "[^\\d]")) 

library(igraph)
library(ggraph)

abs_word_pairs <- wordf %>%
  pairwise_count(word,line,sort = TRUE)

set.seed(42)
abs_word_pairs %>%
  filter(n >= 9) %>%
  graph_from_data_frame() %>%
  ggraph(layout = "fr") +
  geom_edge_link(aes(edge_alpha = n, edge_width = n), edge_colour = "cyan4") +
  geom_node_point(size = 1) +
  geom_node_text(aes(label = name), repel = TRUE, 
                 point.padding = unit(0.2, "lines")) +
  labs(title = "Bigrams in abstract") +
  theme_void()

##

words_by_journal <- wordf %>%
  count(line, word, sort = TRUE) %>%
  ungroup()

tf_idf <- words_by_journal %>%
  bind_tf_idf(line, word, n) %>%
  arrange(desc(tf_idf))

tf_idf %>%
  group_by(line) %>%
  top_n(10, tf_idf) %>%
  ungroup() %>%
  mutate(word = reorder(word, tf_idf)) %>%
  ggplot(aes(word, tf_idf, fill = line)) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ line, scales = "free") +
  ylab("tf-idf") +
  coord_flip()
